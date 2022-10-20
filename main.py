import os
import shutil
import streamlit as st
from github import Github
import networkx as nx
import networkx as nx


client = Github(st.secrets["ACCESS_TOKEN"], per_page=100)


def main():
	st.warning('Higher Followers or stars will slow down the execution,', icon="⚠️")
    USER = st.text_input("Enter Github Username : ", value="99SharmaTushar")
    REPO = st.text_input("Enter Github Repo : ",
                         value="Codeforces-Performace-Analyser")
    st.header("Visualising Stargazer Network : ")
    if st.button("Visualize"):
        user = client.get_user(USER)
        repo = user.get_repo(REPO)

        g_stargazers = nx.DiGraph()
        g_stargazers.add_node(repo.name + '(repo)', type='repo',
                              lang=repo.language, owner=user.login)
        stargazers = [s for s in repo.get_stargazers()]
        st.write(f"Number of stargazers : {len(stargazers)}")
        for sg in stargazers:
            g_stargazers.add_node(sg.login + '(user)', type='user')
            g_stargazers.add_edge(
                sg.login + '(user', repo.name + '(repo)', type='gazes')
        gp = nx.complete_graph(g_stargazers)
        dot = nx.nx_pydot.to_pydot(gp)
        st.graphviz_chart(dot.to_string())

    st.title("User Specifc Analysis : ")
    USER = st.text_input("Enter Github Username : ", value="jhasiddhant")
    user = client.get_user(USER)

    st.header("Visualizing Follower Network : ")
    if st.button("Visualize Network"):
        g_followers = nx.Graph()
        g_followers.add_node(user.login+'(user)', type='user')
        followers = [s for s in user.get_followers()]
        st.write(f"Number of Followers : {len(followers)}")
        for follower in followers:
            g_followers.add_node(follower.login+'(user)', type='user')
            g_followers.add_edge(follower.login+'(user)',
                                 user.login+'(repo)', type='follows')
        gp = nx.complete_graph(g_followers)
        dot = nx.nx_pydot.to_pydot(gp)
        st.graphviz_chart(dot.to_string())

        for follower in followers:
            followers_2 = [s for s in follower.get_followers()]
            for follower_2 in followers_2:
                g_followers.add_node(follower_2.login+'(user)', type='user')
                g_followers.add_edge(follower_2.login+'(user)',
                                     follower.login+'(repo)', type='follows')
        gp = nx.complete_graph(g_followers)
        dot = nx.nx_pydot.to_pydot(gp)
        st.graphviz_chart(dot.to_string())


if __name__ == '__main__':
    st.title("Social Network Analysis on Github Users")
    main()
    st.markdown(
        """
			<style>
	a:link , a:visited{
	color: blue;
	background-color: transparent;
	text-decoration: underline;
	}

	a:hover,  a:active {
	color: red;
	background-color: transparent;
	text-decoration: underline;
	}

	.footer {
	position: fixed;
	left: 0;
	bottom: 0;
	width: 100%;
	background-color: white;
	color: black;
	text-align: center;
	}
	</style>
	<div class="footer">
	<p>Developed @ IIIT-Kota</p>
	</div>
""", unsafe_allow_html=True)
