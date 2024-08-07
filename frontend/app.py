import streamlit as st
import requests

# Backend URL
backend_url = 'https://e353-2401-4900-1c43-8452-65df-6d65-1883-d76a.ngrok-free.app'  # Replace with your ngrok URL

def login(username, password):
    response = requests.post(f'{backend_url}/login', json={'username': username, 'password': password})
    return response.json()

def register(username, password):
    response = requests.post(f'{backend_url}/register', json={'username': username, 'password': password})
    return response.json()

def generate_story(characters, scene, scenario, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{backend_url}/generate', json={'characters': characters, 'scene': scene, 'scenario': scenario}, headers=headers)
    return response.json()

def fetch_stories(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{backend_url}/stories', headers=headers)
    return response.json()

def save_story(title, content, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{backend_url}/save', json={'title': title, 'content': content}, headers=headers)
    return response.json()

def generate_image(prompt, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{backend_url}/generate_image', json={'prompt': prompt}, headers=headers)
    return response.json()

def save_as_pdf(title, text, image_path, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{backend_url}/save_as_pdf', json={'title': title, 'text': text, 'image_path': image_path}, headers=headers)
    return response.json()

# Main Streamlit app
def main():
    st.title("TaleTailor AI")

    if 'token' not in st.session_state:
        st.session_state.token = None
        st.session_state.characters = [{'name': '', 'emotions': {'happiness': 0, 'sadness': 0, 'fear': 0, 'disgust': 0, 'anger': 0, 'surprise': 0}}]
        st.session_state.scene = ''
        st.session_state.scenario = ''
        st.session_state.story = ''
        st.session_state.title = ''
        st.session_state.image_path = ''
        st.session_state.stories = []
        st.session_state.selected_story = ''
        st.session_state.username = ''
        st.session_state.password = ''

    # Authentication
    username = st.text_input("Username", value=st.session_state.username, key="username")
    password = st.text_input("Password", type="password", value=st.session_state.password, key="password")

    if st.session_state.token:
        st.write("Logged in")
    else:
        if st.button("Register"):
            register_response = register(username, password)
            st.write(register_response)

        if st.button("Login"):
            login_response = login(username, password)
            if 'access_token' in login_response:
                st.session_state.token = login_response['access_token']
                st.write("Logged in")
            else:
                st.write(login_response)
        return  # Stop the execution here if not logged in

    # Characters input
    st.subheader("Characters")
    characters = []
    num_characters = st.number_input("Number of Characters", min_value=1, max_value=10, step=1, value=len(st.session_state.characters))

    if num_characters > len(st.session_state.characters):
        for _ in range(num_characters - len(st.session_state.characters)):
            st.session_state.characters.append({'name': '', 'emotions': {'happiness': 0, 'sadness': 0, 'fear': 0, 'disgust': 0, 'anger': 0, 'surprise': 0}})
    elif num_characters < len(st.session_state.characters):
        st.session_state.characters = st.session_state.characters[:num_characters]

    for i in range(num_characters):
        character_name = st.text_input(f"Character {i+1} Name", value=st.session_state.characters[i]['name'], key=f'char_name_{i}')
        emotions = {
            'happiness': st.slider(f"Happiness of {character_name}", 0, 100, st.session_state.characters[i]['emotions']['happiness'], key=f'happiness_{i}'),
            'sadness': st.slider(f"Sadness of {character_name}", 0, 100, st.session_state.characters[i]['emotions']['sadness'], key=f'sadness_{i}'),
            'fear': st.slider(f"Fear of {character_name}", 0, 100, st.session_state.characters[i]['emotions']['fear'], key=f'fear_{i}'),
            'disgust': st.slider(f"Disgust of {character_name}", 0, 100, st.session_state.characters[i]['emotions']['disgust'], key=f'disgust_{i}'),
            'anger': st.slider(f"Anger of {character_name}", 0, 100, st.session_state.characters[i]['emotions']['anger'], key=f'anger_{i}'),
            'surprise': st.slider(f"Surprise of {character_name}", 0, 100, st.session_state.characters[i]['emotions']['surprise'], key=f'surprise_{i}'),
        }
        characters.append({'name': character_name, 'emotions': emotions})
    st.session_state.characters = characters
    
    scene = st.text_input("Scene", value=st.session_state.scene, key="scene_input")
    st.session_state.scene = scene
    scenario = st.text_input("Scenario", value=st.session_state.scenario, key="scenario_input")
    st.session_state.scenario = scenario

    if st.button("Generate Story"):
        story_response = generate_story(characters, st.session_state.scene, st.session_state.scenario, st.session_state.token)
        if 'story' in story_response:
            st.session_state.story = story_response['story']
            st.write(st.session_state.story)
        else:
            st.write(story_response)

    title = st.text_input("Title", value=st.session_state.title, key="title_input")
    st.session_state.title = title

    if st.button("Save Story"):
        save_response = save_story(st.session_state.title, st.session_state.story, st.session_state.token)
        st.write(save_response)

    if st.button("Generate Image"):
        prompt = " ".join(st.session_state.story.split()[:10])
        image_response = generate_image(prompt, st.session_state.token)
        if 'image_path' in image_response:
            st.session_state.image_path = image_response['image_path']
            st.image(f"{backend_url}/{st.session_state.image_path}")
        else:
            st.write(image_response)

    if st.button("Save as PDF"):
        pdf_response = save_as_pdf(st.session_state.title, st.session_state.story, st.session_state.image_path, st.session_state.token)
        if 'pdf_path' in pdf_response:
            pdf_link = f"{backend_url}/{pdf_response['pdf_path']}"
            st.markdown(f"[Download PDF]({pdf_link})")
        else:
            st.write(pdf_response)

    if st.button("Fetch Stories"):
        stories_response = fetch_stories(st.session_state.token)
        if 'stories' in stories_response:
            st.session_state.stories = stories_response['stories']
            st.session_state.selected_story = ''
        else:
            st.write(stories_response)

    if st.session_state.stories:
        for story in st.session_state.stories:
            if st.button(f"Display {story['title']}"):
                st.session_state.selected_story = story.get('content', 'Content not available')
                st.write(st.session_state.selected_story)

    if st.session_state.selected_story:
        st.subheader("Displayed Story")
        st.write(st.session_state.selected_story)

if __name__ == "__main__":
    main()
