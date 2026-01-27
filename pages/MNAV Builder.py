import streamlit as st
from streamlit_tags import st_tags
from utils.data_utils import read_environment_variables, store_environment_variables, clear_env_vars
st.set_page_config(
    page_title="Mental Navigation Task",
    layout="wide",
)

st.title("Mental Navigation Builder")
project_name = "mental-nav"

environments = [
    {
        "name": "With Dots",
        "tag": "env_dots",
        "urls": [f"https://mentalnavigation.web.app/?DAY={i}&ENV=env_dots" for i in range(1, 5)],
    },
    {
        "name": "Without Dots",
        "tag": "env_no_dots",
        "urls": [f"https://mentalnavigation.web.app/?DAY={i}&ENV=env_no_dots" for i in range(1, 5)],
    },
]

cols = st.columns(len(environments), gap="large")

if "show_links" not in st.session_state:
    st.session_state.show_links = {}
if "edit_env" not in st.session_state:
    st.session_state.edit_env = None

def toggle_links(env_name):
    st.session_state.show_links[env_name] = not st.session_state.show_links.get(env_name, False)

for col, env in zip(cols, environments):
    env_name = env["name"]
    is_editing = st.session_state.edit_env is not None and st.session_state.edit_env["name"] == env_name

    with col:
        with st.container(border=True):
            st.markdown(f"### {env_name}")

            buttonCols = st.columns(2, gap="small")

            # ---- Edit button ----
            with buttonCols[0]:
                if st.button("Edit", key=f"edit_{env_name}"):
                    st.session_state.edit_env = env
                    # hide links when editing starts
                    st.session_state.show_links[env_name] = False
                    st.rerun()

            # ---- Show/Hide links button (hidden when editing) ----
            if not is_editing:
                with buttonCols[1]:
                    st.button(
                        "Hide links" if st.session_state.show_links.get(env_name, False) else "Show links",
                        key=f"preview_{env_name}",
                        on_click=toggle_links,
                        args=(env_name,),
                    )

            # ---- Render links (hidden when editing) ----
            if not is_editing and st.session_state.show_links.get(env_name, False):
                st.divider()
                for day, url in enumerate(env["urls"], start=1):
                    st.link_button(
                        label=f"DAY {day}",
                        url=url,
                        use_container_width=True,
                    )

edit_env = st.session_state.edit_env
imageset_options = [1,2,3]
 
if edit_env:
    with st.form('experiment'):
        st.markdown(f"## Environment: {edit_env['name']} ")
        env_vars = read_environment_variables(project_name,edit_env['tag'])
        imageset = st.selectbox("Imageset", imageset_options, index=imageset_options.index(env_vars.get('imageset',1)))
        # trainingStepSizes = lst.multiselect("Training Step Sizes", [12.5, 15, 17.5, 20], default=[12.5, 15])
        # testingStepSizes = st.multiselect("Testing Step Sizes", [10, 12.5, 15, 17.5, 22.5, 27.5, 30], default=[10, 12.5, 15, 17.5, 22.5, 27.5])
        trainingStepSizes = st_tags(
            label="Training Speeds (cm/s)",
            text="Press enter to add more",
            value = [str(x) for x in env_vars.get('trainingStepSizes',["10", "20"])],
            suggestions=["10",  "20"],
        )
        testingStepSizes = st_tags(
            label="Testing Speeds (cm/s)",
            text="Press enter to add more",
            value = [str(x) for x in env_vars.get('testingStepSizes',["10", "20"])],
            suggestions=["10", "20"],
        )

        interLandmarkDistance = st.number_input("Inter-Landmark Distance (cm)", value=env_vars.get('interLandmarkDistance', 5), min_value=5, max_value=30)

        numLandmarks = st.slider("Number of Landmarks", value=env_vars.get('numLandmarks', 9),min_value=2,max_value=9)
        # day = st.selectbox("Day", [1, 2, 3, 4, 5])
        screenHeightcm = st.number_input("Screen Height (cm)", value=env_vars.get('screenHeightcm', 21.24))
        # if day<3:
        #     numTrialPairs = st.slider("Number of Trial Pairs",max_value=int(numLandmarks*(numLandmarks-1)/2))
        #     initialTrials = st.slider("Initial Trials", max_value=100)
    
        submitted = st.form_submit_button("Submit")

 
        if submitted:
            
            if trainingStepSizes:
                try:
                    trainingStepSizes = list(map(float, trainingStepSizes))
                except ValueError:
                    st.error("Invalid training speeds. Please enter numeric values.")
                    st.stop()

            if testingStepSizes:
                try:
                    testingStepSizes = list(map(float, testingStepSizes))
                except ValueError:
                    st.error("Invalid testing speeds. Please enter numeric values.")
                    st.stop()

            formData = {
                "imageset": imageset,
                "trainingStepSizes": trainingStepSizes,
                "testingStepSizes": testingStepSizes,
                "interLandmarkDistance":interLandmarkDistance,
                "numLandmarks": numLandmarks,
                "screenHeightcm": screenHeightcm,
            }
            env_vars.update(formData)
            store_environment_variables(project_name, edit_env['tag'], env_vars)

            # ✅ hide form
            st.session_state.edit_env = None
            st.session_state.form_success = True

            st.rerun()

if st.session_state.get('FormSubmitter:experiment-Submit'):
    st.text("Environment updated successfully!")
    


# TODO:
# Record Completion code to fire base


# features to edit:

# Speed 
# interlm distance
# screen resolution
# screen height 

# read from firebase and extract the features
# display the features in a form
# on submit, update the firebase document

