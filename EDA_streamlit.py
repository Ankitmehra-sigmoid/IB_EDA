import streamlit as st
from EDA_streamlit_utils import standerdize_cols,grouping,plot_warehouse_yearly_quantity_3,plot_bar,plot_heatmap
import pandas as pd
import plotly.express as px

############# Reading data and preprocessing######
df_in=pd.read_csv('Cargosoft-Data_2022-2024.csv',encoding='mixed')
df_in['Creation Date'] = pd.to_datetime(df_in['Creation Date'])
df_in=standerdize_cols(df=df_in,selected_cols=['Place of delivery','Place of loading'])
df_in['year']=df_in['Creation Date'].dt.year
df_in=df_in[df_in['year']>=2022]
print(df_in)
#######################################
# def chart_1(year):
#     df=df_in[df_in['year'].isin(year)]
#     grouped_df=grouping(df=df,
#                         group_by_1='Place of loading',
#                         group_by_2='year',
#                         target_col='Packages')
#     plot_warehouse_yearly_quantity_3(df=grouped_df,x='Place of loading', y='Packages', breakdown_col='year', df_in=df_in, is_percent=False,title='Top 5 Loading Locations')

def chart_1(year,loading_l):
    df=df_in[df_in['year'].isin(year)]
    df=df[df['Place of loading'].isin(loading_l)]
    grouped_df=grouping(df=df,
                        group_by_1='Place of loading',
                        group_by_2='year',
                        target_col='Packages')
    plot_bar(data=grouped_df,field='Place of loading',metric='Packages',aggrigation='sum',top=5,percent=True)


######################################

def chart_2(year,delivery_l):
    df=df_in[df_in['year'].isin(year)]
    
    df=df[df['Place of delivery'].isin(delivery_l)]
    
    grouped_df=grouping(df=df,
                        group_by_1='Place of delivery',
                        group_by_2='year',
                        target_col='Packages')
    plot_bar(data=grouped_df,field='Place of delivery',metric='Packages',aggrigation='sum',top=5,percent=True)
######################################
def chart_3(year,loading_l,delivery_l, radio_selection):
    df=df_in[df_in['year'].isin(year)]
    df=df[df['Place of loading'].isin(loading_l)]
    df=df[df['Place of delivery'].isin(delivery_l)]
    if  radio_selection=='Percentage':
        gr_type=True
    else:
        gr_type=False
    grouped_df=grouping(df=df,
                        group_by_1='Place of loading',
                        group_by_2='Place of delivery',
                        target_col='Packages')
    plot_heatmap(data=grouped_df,field1='Place of delivery',field2='Place of loading',metric='Packages',aggrigation='sum',top=10,percent=gr_type)

######################################
def chart_4(year,loading_l,breadown_selection):
    df=df_in[df_in['year'].isin(year)]
    df=df[df['Place of loading'].isin(loading_l)]
    grouped_df=grouping(df=df,
                        group_by_1='Place of loading',
                        group_by_2=breadown_selection,
                        target_col='Packages')
    plot_warehouse_yearly_quantity_3(df=grouped_df,x='Place of loading', y='Percentage', breakdown_col=breadown_selection, df_in=df_in, is_percent=True,title='Loading Locations Breakdown By Loading Type')
######################################
def chart_5(year,delivery_l,breadown_selection):
    df=df_in[df_in['year'].isin(year)]
    df=df[df['Place of delivery'].isin(delivery_l)]
    grouped_df=grouping(df=df,
                        group_by_1='Place of delivery',
                        group_by_2=breadown_selection,
                        target_col='Packages')
    plot_warehouse_yearly_quantity_3(df=grouped_df,x='Place of delivery', y='Percentage', breakdown_col=breadown_selection, df_in=df_in, is_percent=True,title='Delivery Locations Breakdown By Loading Type')
####################################
def chart_6(year):
    df=df_in[df_in['year'].isin(year)]
    grouped_df=grouping(df=df,
                        group_by_1='Product group',
                        group_by_2='year',
                        target_col='Packages')
    plot_warehouse_yearly_quantity_3(df=grouped_df,x='Product group', y='Packages', breakdown_col='year', df_in=df_in, is_percent=False,title='Top 5 Product Groups')
####################################
def chart_7(year):
    df=df_in[df_in['year'].isin(year)]
    grouped_df=grouping(df=df,
                        group_by_1='Place of delivery',
                        group_by_2='Product group',
                        target_col='Packages')
    plot_warehouse_yearly_quantity_3(df=grouped_df,x='Place of delivery', y='Percentage', breakdown_col='Product group', df_in=df_in, is_percent=True,title='Product group distribution for WH')

def main():
    
    st.set_page_config(
        page_title="Multi-Page Streamlit App",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("IB Data EDA")

    # Create a sidebar with page selection
    page = st.sidebar.radio("Select Page", ["Inbound", "Internal Transfer"])

    # Display different content based on the selected page
    if page == "Inbound":
       
        st.header("Inbound")
        col_y, col_p,col_d = st.beta_columns(3)
        with col_y:
            st.write('Year')
            options = [2022,2023,2024]
            year = st.multiselect(
                label='Select your options',
                options=options,
                default=[2022,2023,2024]  # You can set default selections here
            )
        with col_p:
            st.write('Loading Locations')
            options = df_in['Place of loading'].unique()
            loading_l = st.multiselect(
                label='Select your options',
                options=options,
                default=['RADOM', 'TARNOWO PODGORNE', 'LANGENHAGEN', 'MANISA', 'HAMBURG'])
        with col_d:
            st.write('Delivery Locations')
            options = df_in['Place of delivery'].unique()
            delivery_l = st.multiselect(
                label='Select your options',
                options=options,
                default=['LANGENHAGEN', 'KREFELD', 'MEERANE', 'SCHWIEBERDINGEN', 'DREIEICH'])

        # st.write("You selected:", year)
        
        col1, col2 = st.beta_columns(2)
        ################################
        with col1:
            chart_1(year,loading_l)
            st.write('Radom and Tarnowo are the major loading locations constituting for ~90 percent of overall packages')
            

        with col2:
            chart_2(year,delivery_l)
            st.write('Langanhagen is the top delivery location, receiving ~42 percent of ovrall packages ')
        ###################################
        radio_options = ["Percentage","Units" ]
        radio_selection = st.radio("Choose an option:", radio_options)
        chart_3(year,loading_l,delivery_l, radio_selection)
        st.write('1.Radom to Langanhagen is the leading lane for inbound.')
        st.write('2.Langenhagen is the only delivery location that receives inboud from all top 5 Factories')
        st.write('3.Langenhagen received overall 41.84 percent from 2022-2024 out of which 37.89 percent came from top 5 factories')
       
        breakdown_cols=['Type of Loading','Product group']
        breadown_selection = st.radio("Choose an option:", breakdown_cols)
        col3, col4 = st.beta_columns(2)
        
        with col3:
            chart_4(year,loading_l,breadown_selection)
            
        with col4:
            chart_5(year,delivery_l,breadown_selection)
            
        # col5, col6 = st.beta_columns(2)
        # with col5:
        #     chart_6(year)
            
        
            
            
        # # internal_transfer()
        # user_input = st.number_input("Enter an integer", value=5, step=1)
        # st.write("total number of DC:", int(user_input))
        # if st.button("Click To Run The optimization"):
        #     New_Warehouse_location(num_warehouse=user_input)
        

    # elif page == "Internal Transfer":
    #     st.header("Page 2")
    #     col1, col2 = st.beta_columns(2)
    #     with col1:
    #         geospatial_analysis(chart=1)
    #     with col2:
    #         geospatial_analysis(chart=2)







    

# Run the Streamlit app
# if st.button("Click To Run The APP"):
if __name__ == "__main__":
    main()
