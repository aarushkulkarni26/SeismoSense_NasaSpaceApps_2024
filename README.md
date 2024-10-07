# SeismoSense

https://docs.google.com/presentation/d/1nTfbbUrOi_6UKlrDTOFkRxPZ6v4_i4OmicbySvhx0c8/

We developed an STA/LTA model for detecting the start time of a moon/marsquake from the sensor data locally. This is needed for better seismology analysis on other planets, where large amount of data cannot be transferred back to Earth due to power constraints. We also implemented the LSTM algorithm, but the STA/LTA model was less susceptible to the data augmentations. We used Flask for our backend and Streamlit for our frontend. The models were trained on Kaggle and the full app was developed on VS Code. In summary, we would aid planetary seismology missions by reducing the amount of continuous time data sent back to Earth. One challenge we faced was dealing with the noisy and missing portions of the real-time data in the test cases for moonquakes.
