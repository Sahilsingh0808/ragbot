# ... existing code ...

# Display Chat History
st.markdown("### Chat History")
st.divider()

for chat in reversed(st.session_state.conversation_history):
    if chat["role"] == "user":
        message(chat["content"], is_user=True, key=f"user-{chat}")
    else:
        col1, col2 = st.columns([6, 1])
        with col1:
            message(chat["content"], key=f"bot-{chat}")
        with col2:
            # Compact reaction buttons
            button_container = st.container()
            with button_container:
                st.markdown("""
                    <style>
                    .reaction-group { display: flex; gap: 4px; }
                    .reaction-button { padding: 2px 4px; opacity: 0.6; cursor: pointer; }
                    .reaction-button:hover { opacity: 1; }
                    </style>
                    <div class="reaction-group">
                    """, unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1,1,1])
                with c1:
                    if st.button("👍", key=f"like-{chat}", help="Like"):
                        st.success("Liked!")
                with c2:
                    if st.button("👎", key=f"dislike-{chat}", help="Dislike"):
                        st.warning("Disliked")
                with c3:
                    if st.button("⭐", key=f"favorite-{chat}", help="Favorite"):
                        st.session_state.favorite_responses.append(chat["content"])
                        st.info("Added!")

# ... existing code ...