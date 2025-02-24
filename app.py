import streamlit as st
import pandas as pd
import plotly.express as px
import io
from PIL import Image
import plotly.io as pio


# Set page configuration
st.set_page_config(page_title="Data Visualization App", layout="wide")

# Add title and description
st.title("📊 Data Visualization App")
st.write("Use the sidebar to upload data and customize your visualization!")

# upload file
st.sidebar.title('📁 Upload File')
uploaded_file = st.sidebar.file_uploader("Choose a file",type=['csv','xlsx'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error: {e}")

    #display the basic information
    st.write('📋 Dataset Information')
    st.write(f'Number of rows: {df.shape[0]}')
    st.write(f'Number of columns: {df.shape[1]}')
    st.write('## Dataset preivew')
    st.dataframe(df.head())

    # sidebar of data cleaning
    st.sidebar.header('Data cleaning')
    cleaning = st.sidebar.radio('Select Cleaning Options:',
            ['No cleaning','Remove missing values','Remove duplicates']
       )

    # Apply data cleaning
    if cleaning == 'Remove missing values':
        df = df.dropna()
        st.success('missing values removed')
    elif cleaning == 'Remove duplicates':
        df = df.drop_duplicates()
        st.success('Duplicates removed')

    # get numeric columns 
    numeric_columns=df.select_dtypes(include=['float','int']).columns
            

    # Sidebar for selection of chart 
    st.sidebar.header('Chart Selection')
    chart_type =st.sidebar.selectbox('Select chart type:',
        ['Bar chart','Line chart','Histogram','scatter plot']
     )

        # chart creation
    st.write('### Chart Visualization')
    fig =None

    if chart_type in ['bar chart','Line chart','Scatter plot','Histogram']:
           x_col =st.sidebar.selectbox('Select x-axis column',df.columns)
           y_col =st.sidebar.selectbox('Select y-axis column',numeric_columns)
        

           if chart_type == 'Bar Chart':
                fig =px.bar(df,x=x_col,y=y_col,title='Bar chart')
           elif chart_type == 'Line chart':
                fig =px.line(df,x=x_col,y=y_col,title='Line chart')
           else:
            fig =px.scatter(df,x=x_col,y=y_col,title='Scatter plot')
    else:
           col = st.sidebar.selectbox('Select column',numeric_columns)
           fig = px.histogram(df,x=col,title='Histogram')
                
        # Display the chart
    if fig:
        st.plotly_chart(fig, use_container_width=True)

        # Add download options to sidebar
        with st.sidebar:
            st.header("💾 Download Chart")
            
            try:
                # Convert chart to image
                img_bytes = pio.to_image(fig, format="png")
                img = Image.open(io.BytesIO(img_bytes))
                
                # PNG download
                png_buffer = io.BytesIO()
                img.save(png_buffer, format='PNG')
                png_buffer.seek(0)
                st.download_button(
                    label="Download as PNG",
                    data=png_buffer,
                    file_name=f"chart_{chart_type.lower().replace(' ', '_')}.png",
                    mime="image/png",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating PNG: {e}")
                st.warning("Please ensure the `kaleido` package is installed and working.")      
    
else:
     st.info('please upload a csv or Excel file to start.')
           
                          
           
                
                     