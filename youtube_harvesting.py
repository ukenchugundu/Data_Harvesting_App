import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

# Add custom Streamlit styles and a header
st.markdown(
    """
    <style>
    .main {
        background-color:black;
    }
    .stSidebar {
        background-color: #e3e6ea;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 4px 8px;
        border-bottom: 1px solid #ddd;
        text-align: left;
        font-size: 13px;
        line-height: 1.1;
        vertical-align: middle;
    }
    th {
        background-color: #2980b9;
        color: white;
    }
    tr:hover {background-color: black;}
    .footer {text-align:center; color:#888; margin-top:40px;}
    .read-more-link { color: #2980b9; text-decoration: underline; cursor: pointer; }
    </style>
    """,
    unsafe_allow_html=True
)

# App header
st.markdown("""
<div style='text-align:center;'>
    <h1 style='color:#2980b9;'>YouTube Data Harvesting App</h1>
    <p style='font-size:18px;'>Fetch and explore videos from any YouTube channel.<br>Enter a channel ID, choose options, and view results instantly!</p>
</div>

""", unsafe_allow_html=True)

# Set up API
api_key = st.secrets["API_KEY"]  # Replace with your actual API key
youtube = build('youtube', 'v3', developerKey=api_key)

# Sidebar input
st.sidebar.header('📺 YouTube Data Harvesting')
st.sidebar.write("<span style='color:#2980b9'>Enter a YouTube channel ID to fetch its videos.</span>", unsafe_allow_html=True)
channel_id = st.sidebar.text_input("Channel ID", "UCuQV3NTfCMmZ18pnskYAc1Q")


max_results = 8  # Show 8 videos related to the content
show_titles_only = st.sidebar.checkbox("Show only video titles", value=False)



# Fetch channel videos
def get_channel_videos(channel_id):
    # Get uploads playlist ID
    res = youtube.channels().list(id=channel_id, part='contentDetails,statistics').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    subscribers = res['items'][0]['statistics'].get('subscriberCount', 'N/A')

    # Get videos from the playlist
    videos = []
    next_page_token = None
    fetched = 0
    while True:
        pl_request = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=min(max_results - fetched, 50),
            pageToken=next_page_token
        )
        pl_response = pl_request.execute()
        video_ids = [item['snippet']['resourceId']['videoId'] for item in pl_response['items']]
        # Fetch video statistics (likes)
        stats_response = youtube.videos().list(
            id=','.join(video_ids),
            part='statistics'
        ).execute()
        stats_dict = {item['id']: item['statistics'].get('likeCount', 'N/A') for item in stats_response['items']}
        for item in pl_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            like_count = stats_dict.get(video_id, 'N/A')
            title = item['snippet']['title']
            published_at = item['snippet'].get('publishedAt', 'N/A')
            description = item['snippet'].get('description', 'N/A')
            # Add read more link if description is long
            if len(description) > 80:
                short_desc = description[:80].rstrip() + '... '
                read_more = f'<a href="{video_url}" target="_blank" class="read-more-link">Read more</a>'
                description = short_desc + read_more
            thumbnails = item['snippet']['thumbnails']['default']['url'] if 'thumbnails' in item['snippet'] and 'default' in item['snippet']['thumbnails'] else 'N/A'
            videos.append({
                'title': title,
                'video_id': video_id,
                'video_url': video_url,
                'subscribers': subscribers,
                'likes': like_count,
                'published_at': published_at,
                'description': description,
                'thumbnail': thumbnails
            })
            fetched += 1
            if fetched >= max_results:
                break
        if fetched >= max_results:
            break
        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:
            break
    return pd.DataFrame(videos)

# Fetch related videos for a given video ID
def get_related_videos(video_id):
    search_response = youtube.search().list(
        relatedToVideoId=video_id,
        part='snippet',
        type='video',
        maxResults=5
    ).execute()
    related = []
    for item in search_response['items']:
        rel_video_id = item['id']['videoId']
        rel_title = item['snippet']['title']
        rel_url = f"https://www.youtube.com/watch?v={rel_video_id}"
        related.append({'title': rel_title, 'video_url': rel_url})
    return pd.DataFrame(related)


st.markdown("<h2 style='color:#2980b9;'>YouTube Channel Videos</h2>", unsafe_allow_html=True)
if channel_id:
    # Remove search bar at top right, add search button under channel input
    st.sidebar.write("")
    # Remove search from sidebar, move to cards section
    search_query = ""
    search_button = False
    with st.spinner("Fetching videos..."):
        data = get_channel_videos(channel_id)
    if not data.empty:
        if show_titles_only:
            # Add search input and button above titles in one line using Streamlit columns
            search_col = st.container()
            with search_col:
                search_input, search_btn = st.columns([5,1])
                search_query = search_input.text_input(
                    "",
                    value="",
                    key="search_title_input",
                    help="Type to filter videos by title",
                    placeholder="Search video titles..."
                )
                search_button = search_btn.button("Search", key="search_button")
            # Only filter when search button is pressed or if search_query is not empty
            if search_button or search_query:
                active_search = search_query
            else:
                active_search = ""
            # Filter titles by search query (case-insensitive)
            filtered_titles = data['title'][data['title'].str.contains(active_search, case=False, na=False)] if active_search else data['title']
            st.markdown("<div style='margin-top:24px;'>", unsafe_allow_html=True)
            for i, title in enumerate(filtered_titles):
                st.markdown(f"""
                <div style='width:100%; margin-bottom:14px;'>
                    <div style='background:#23272b; border-radius:10px; box-shadow:0 1px 6px rgba(41,128,185,0.10); padding:12px 18px; font-size:16px; color:#fff; border:1.5px solid #2980b9; display:flex; align-items:center;'>
                        <span style='width:100%; white-space:nowrap; overflow-x:auto; text-overflow:ellipsis;'>{title}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:#2980b9;'>Videos</h3>", unsafe_allow_html=True)
            # Add search input and button above cards in one line using Streamlit columns
            search_col = st.container()
            with search_col:
                search_input, search_btn = st.columns([5,1])
                search_query = search_input.text_input(
                    "",
                    value="",
                    key="search_title_input",
                    help="Type to filter videos by title",
                    placeholder="Search video titles..."
                )
                search_button = search_btn.button("Search", key="search_button")
            # Only filter when search button is pressed or if search_query is not empty
            if search_button or search_query:
                active_search = search_query
            else:
                active_search = ""
            if 'card_offset' not in st.session_state:
                st.session_state.card_offset = 0
            cards_per_page = 6
            # Filter data by search query (case-insensitive)
            filtered_data = data[data['title'].str.contains(active_search, case=False, na=False)] if active_search else data
            total_videos = len(filtered_data)
            end_offset = st.session_state.card_offset + cards_per_page
            show_data = filtered_data.iloc[:end_offset]
            if show_data.empty:
                st.info("No videos found matching your search. Try a different keyword or check the channel's content.")
            else:
                card_html = ""
                for _, row in show_data.iterrows():
                    card_html += f"""
                    <div style='background:#222; border-radius:8px; padding:16px; margin-bottom:16px; color:#fff;'>
                        <div style='display:flex; align-items:center;'>
                            <img src='{row['thumbnail']}' style='width:120px; height:90px; border-radius:6px; margin-right:16px;'>
                            <div>
                                <h4 style='margin:0; color:#2980b9;'>{row['title']}</h4>
                                <p style='margin:4px 0 8px 0; font-size:13px;'>{row['description']}</p>
                                <a href='{row['video_url']}' target='_blank' style='color:#2980b9; text-decoration:underline;'>Watch on YouTube</a>
                                <br>
                                <a href='{row['video_url']}' target='_blank' class='read-more-link' style='font-size:15px; padding:6px 18px; border-radius:6px; background:#2980b9; color:#fff; text-decoration:none; display:inline-block; margin-top:8px;'>Read More</a>
                            </div>
                        </div>
                        <div style='margin-top:8px; font-size:12px;'>
                            <b>Likes:</b> {row['likes']} &nbsp;|&nbsp; <b>Published:</b> {row['published_at']} &nbsp;|&nbsp; <b>Subscribers:</b> {row['subscribers']}
                        </div>
                    </div>
                    """
                st.markdown(card_html, unsafe_allow_html=True)
                if end_offset < total_videos:
                    if st.button("Load More Cards", key="load_more_cards", help="Show more video cards"):
                        st.session_state.card_offset += cards_per_page
                        st.experimental_rerun()
    else:
        st.info("No videos found for this channel.")
else:
    st.warning("Please enter a valid channel ID.")

# Footer
st.markdown("<div class='footer'>Created with ❤️ using Streamlit | &copy; 2025<br>For more info, visit <a href='https://streamlit.io/' target='_blank' class='read-more-link'>Streamlit Docs</a></div>", unsafe_allow_html=True)