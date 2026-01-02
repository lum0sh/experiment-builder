import streamlit as st

st.set_page_config(
    page_title="Mental Navigation Task",
    layout="wide",
)

st.title("Mental Navigation Builder")

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

for col, env in zip(cols, environments):
    with col:
        with st.container(border=True):
            st.markdown(f"### {env['name']}")

            st.divider()

            for day, url in enumerate(env["urls"], start=1):
                st.link_button(
                    label=f"DAY {day}",
                    url=url,
                    use_container_width=True,
                )


        # if st.button("Edit",key=f"edit_{env['name']}"):
        #     edit_env = env

# status_text = st.text("Status: Ready")

# if edit_env:
#     st.text(f"Edit {edit_env['name']} ")
#     with st.form('experiment'):
#         imageset = st.selectbox("Imageset", [1,2,3])
#         trainingStepSizes = st.multiselect("Training Step Sizes", [12.5, 15, 17.5, 20], default=[12.5, 15])
#         testingStepSizes = st.multiselect("Testing Step Sizes", [10, 12.5, 15, 17.5, 22.5, 27.5, 30], default=[10, 12.5, 15, 17.5, 22.5, 27.5])
#         numLandmarks = st.slider("Number of Landmarks", value=9,min_value=2,max_value=9)
#         day = st.selectbox("Day", [1, 2, 3, 4, 5])
#         screenHeightcm = st.number_input("Screen Height (cm)", value=21.24)
#         # if day<3:
#         #     numTrialPairs = st.slider("Number of Trial Pairs",max_value=int(numLandmarks*(numLandmarks-1)/2))
#         #     initialTrials = st.slider("Initial Trials", max_value=100)
        

#         submitted = st.form_submit_button("Submit")

#         if submitted:
#             formData = {
#                 # "imageset": imageset,
    
#                 "trainingStepSizes": ",".join(map(str, trainingStepSizes)),
#                 "testingStepSizes": ",".join(map(str, testingStepSizes)),
#                 # "numTrialPairs": numTrialPairs,
#                 "numLandmarks": numLandmarks,
#                 # "initialTrials": initialTrials,
#                 "screenHeightcm": screenHeightcm,
#                 "DAY": day
#             }


#     if submitted:
#         # edit_env = ''
#         status_text.text("Save to database.")
#         # st.
#         # st.link_button("Go to experiment", generate_experiment_link(experiment_URL,  formData))

