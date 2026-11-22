import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Youtube Video&Comment Analysis")

video_url = st.sidebar.text_input("Paste Url Here: ")

if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis=False
if 'video_df' not in st.session_state:
    st.session_state.video_df = None
if 'df' not in st.session_state:
    st.session_state.df = None

if st.sidebar.button('Show Analysis'):
    if video_url.strip():
        video_df = preprocessor.preprocess_video(video_url)
        df = preprocessor.preprocess_comments(video_url)
        st.session_state.video_df = video_df
        st.session_state.df = df
        st.session_state.show_analysis = True
    else:
        st.warning("Please enter a valid Youtube URL.")
if st.session_state.show_analysis:
    video_df = st.session_state.video_df
    df = st.session_state.df
    # with st.spinner("Fetching Youtube Comments..."):
    #     df = preprocessor.preprocess_comments(video_url)
    # st.success('Comments Fetched Successfully')
    user_list = df['user'].unique().tolist()
    # user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis Wrt: ', user_list)
    tab1, tab2 = st.tabs(["Video Analysis", "Comment Analysis"])
    with tab1:
        st.title("Video Analysis")
        st.header(video_df['title'][0])
        col1 = st.columns(1)[0]
        with col1:
            st.metric("Uploaded On: "+str(video_df['upload_date'][0]), '')
        col2, col3, col4= st.columns(3)
        with col2:
            st.metric("Total Duration", str(video_df['duration'][0]))
        with col3:
            st.metric("Total Views", str(video_df['views'][0]))
        with col4:
            st.metric("Total Likes", str(video_df['likes'][0]))

    with tab2:
        st.title("Comment Analysis")
        num_comments, num_words, num_links, num_likes, num_replies = helper.fetch_stats(selected_user, df)
        col5, col6, col7, col11, col12= st.columns(5)
        with col5:
            st.metric("Total Comments", num_comments)
        with col6:
            st.metric("Total Words", num_words)
        with col7:
            st.metric("Total Links", num_links)
        with col11:
            st.metric("Total Likes", num_likes)
        with col12:
            st.metric("Total Replies", num_replies)

        if(selected_user=='Overall'):
            st.title('Most Busy Users')
            x, new_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        try:
            st.title('WordCloud')
            df_wc = helper.create_wordcolud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
        except Exception as e:
            pass
        
        try:
            st.title("Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        except Exception as e:
            pass
        
        try:
            st.title("Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                # ax.bar(emoji_df[0].head(), emoji_df[1].head())
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%.2f')
                st.pyplot(fig)
        except Exception as e:
            pass
        
        try:
            st.title("Yearly Timeline")
            yearly_timeline = helper.yearly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(yearly_timeline['year'], yearly_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        except Exception as e:
            pass
        
        try:
            st.title("Yearly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)
        except Exception as e:
            pass
        