import streamlit as st
from EDA_streamlit_utils import standerdize_cols,grouping,plot_warehouse_yearly_quantity_3,plot_bar,plot_heatmap,side_by_side_bar,plot_donut,create_line_graph
import pandas as pd
import plotly.express as px

############# Reading data and preprocessing######
df_in=pd.read_excel('Cargosoft-Data_2022-2024.xlsx')
df_in=standerdize_cols(df=df_in,selected_cols=['Place of delivery','Place of loading'])
df_in['year']=df_in['Creation Date'].dt.year
df_in['month']=df_in['Creation Date'].dt.month
df_in=df_in[df_in['year']>=2022]
print(df_in)
df_in['loading time']=df_in['Pick up or departed actual']
# df_in['delivery time']=
# df_in['unloading time']=
#######################################Inbound#######################################################################
def chart1(x,y):
    
    side_by_side_bar(df=df_in,x=x,y=y,breakdown_by='year',gr_title='Number of packages by '+x+' and'+' year')


def chart_donut(year,radio_selection):
   df=df_in[df_in['year'].isin(year)]
   plot_donut(data=df,field2=radio_selection,metric='Packages')

def chart_1_1(year,loading_l):
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
def chart_6(year,radio_selection):
    df=df_in[df_in['year'].isin(year)]
    df=df.groupby([radio_selection,'month'])['Packages'].sum().reset_index()
    create_line_graph(df=df, time_col='month', packages_col='Packages', category_col=radio_selection)
    
#######################################################  INTERNAL TRANSFER  #################################################################
df_it=pd.read_excel('Quertransporte_SAP_data.xlsx')
trans_cols=['Werk','Fabrik','Produktgruppe','BME','EME']
df_it=standerdize_cols(df=df_it,selected_cols=trans_cols)
df_it['year']=df_it['Buch.dat.'].dt.year
df_it['month']=df_it['Buch.dat.'].dt.month
df_it['Menge']=df_it['Menge']*(-1)
df_it=df_it[df_it['year']>=2022]
df_it['Werk']=df_it['Werk'].astype('str')


def chart_it1(x,y):
    side_by_side_bar(df=df_it,x=x,y=y,breakdown_by='year',gr_title='Number of packages by '+x+' and'+' year')

def chart_donut_it(year,radio_selection):
   df=df_it[df_it['year'].isin(year)]
   plot_donut(data=df,field2=radio_selection,metric='Menge')



def chart_it3(year):
    df=df_it[df_it['year'].isin(year)]
    grouped_df=grouping(df=df,
                        group_by_1='Werk',
                        group_by_2='Produktgruppe',
                        target_col='Menge')
    plot_warehouse_yearly_quantity_3(df=grouped_df,x='Werk', y='Percentage', breakdown_col='Produktgruppe', df_in=df_in, is_percent=True,title='Breakdown internal transfer qty by warehouse and product group')

def chart_it4(year):
    df=df_it[df_it['year'].isin(year)]
   
    
    grouped_df=grouping(df=df,
                        group_by_1='Werk',
                        group_by_2='Fabrik',
                        target_col='Menge')
    plot_warehouse_yearly_quantity_3(df=grouped_df,x='Werk', y='Percentage', breakdown_col='Fabrik', df_in=df_in, is_percent=True,title='Breakdown internal transfer qty by warehouse and Fabrik')

def chart_it5(year,radio_selection):
    df=df_it[df_it['year'].isin(year)]
    df=df.groupby([radio_selection,'month'])['Menge'].sum().reset_index()
    create_line_graph(df=df, time_col='month', packages_col='Menge', category_col=radio_selection)

def chart_it6(year, percent_or_unit):
    df=df_it[df_it['year'].isin(year)]
    # df=df[df['Werk'].isin()]
    # df=df[df['Fabrik'].isin(delivery_l)]
    if  percent_or_unit=='Percentage':
        gr_type=True
    else:
        gr_type=False
    grouped_df=grouping(df=df,
                        group_by_1='Werk',
                        group_by_2='Fabrik',
                        target_col='Menge')
    plot_heatmap(data=grouped_df,field1='Werk',field2='Fabrik',metric='Menge',aggrigation='sum',top=20,percent=gr_type)
############################################################ OUTBOUND##############################################################################
df_ob_22=pd.read_csv('outbound_processed_2022.csv')
df_ob_23=pd.read_csv('outbound_processed_2023.csv')
df_ob_24=pd.read_csv('outbound_processed_2024.csv')
df_ob_22['year']='2022'
df_ob_23['year']='2023'
df_ob_24['year']='2024'

df_ob=pd.concat([df_ob_22,df_ob_23,df_ob_24])

df_ob['ShPt']=df_ob['ShPt'].astype(int).astype(str)
df_ob['Material']=df_ob['Material'].astype(str)
df_ob['UoM'].replace('ST ', 'ST', inplace=True)
df_ob['UoM'].replace('KG ', 'KG', inplace=True)

df_pm=pd.read_excel('EXPORT 05.01.2024.XLSX')
df_pm=df_pm[['Material','ME','Gebindeinhalt','Packungsinhalt']]
df_pm['PAK to PKT']=df_pm['Packungsinhalt']/df_pm['Gebindeinhalt']
df_pm['Material']=df_pm['Material'].astype(str)
df_ob=pd.merge(df_ob,df_pm,on='Material',how='left')
df_ob['Number of PKT']=df_ob['Packed quantity']/df_ob['Gebindeinhalt']
df_ob['Number of PAK']=df_ob['Packed quantity']/df_ob['Packungsinhalt']
# df_ob['PKT real']=df_ob['Number of PAK']*df_ob['PAK to PKT']
df_ob['Number of PKT']=round(df_ob['Number of PKT'])
df_ob['Number of PAK']=round(df_ob['Number of PAK'])
df_ob['kg gross']=df_ob['Number of PAK']*df_ob['Bruttogewicht PAK']


def chart_ob1(x,y):
    side_by_side_bar(df=df_ob,x=x,y=y,breakdown_by='year',gr_title='Number of PKT by '+x+' and'+' year')


def chart_donut_ob(year,radio_selection):
   df=df_ob[df_ob['year'].isin(year)]
   
   plot_donut(data=df,field2=radio_selection,metric="Number of PKT")

def chart_ob3(year, percent_or_unit):
    df=df_ob[df_ob['year'].isin(year)]
    
    if  percent_or_unit=='Percentage':
        gr_type=True
    else:
        gr_type=False
    grouped_df=grouping(df=df,
                        group_by_1='ShPt',
                        group_by_2='Produkt Typ',
                        target_col="Number of PKT")
    plot_heatmap(data=grouped_df,field1='ShPt',field2='Produkt Typ',metric="Number of PKT",aggrigation='sum',top=20,percent=gr_type)

def main():
    
    st.set_page_config(
        page_title="Multi-Page Streamlit App",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("IB Data EDA")

    # Create a sidebar with page selection
    page = st.sidebar.radio("Select Page", ["Inbound", "Internal Transfer",'Outbound'])

    # Display different content based on the selected page
    if page == "Inbound":
       
        st.header("Cargosoft Data")
        st.table(df_in[:2])
        col_y, col_p,col_d = st.columns(3)
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

        st.write("--------------------------------------------------------------------------------------------")
        
        radio_options = ["Place of loading","Place of delivery",'Product group','Type of Loading','month' ]
        radio_selection = st.radio("Choose an option:", radio_options)
        col1, col2 = st.columns(2)
        with col1:
            chart1(x=radio_selection,y='Packages')
        with col2:
            chart_donut(year,radio_selection)
        st.write('----------------------------------------------------------------------------------------------')    
        chart_6(year,radio_selection)


        col3, col4 = st.columns(2)
        ################################
        with col3:
            chart_1_1(year,loading_l)
            st.write('Radom and Tarnowo are the major loading locations constituting for ~90 percent of overall packages')
            

        with col4:
            chart_2(year,delivery_l)
            st.write('Langanhagen is the top delivery location, receiving ~42 percent of ovrall packages ')
        st.write('----------------------------------------------------------------------------------------------')
        ###################################
        radio_options = ["Percentage","Units" ]
        radio_selection_2 = st.radio("Choose an option:", radio_options)
        chart_3(year,loading_l,delivery_l, radio_selection_2)
        st.write('1.Radom to Langanhagen is the leading lane for inbound.')
        st.write('2.Langenhagen is the only delivery location that receives inboud from all top 5 Factories')
        st.write('3.Langenhagen received overall 41.84 percent from 2022-2024 out of which 37.89 percent came from top 5 factories')
        st.write('----------------------------------------------------------------------------------------------')

        breakdown_cols=['Type of Loading','Product group']
        breadown_selection = st.radio("Choose an option:", breakdown_cols)
        col5, col6 = st.columns(2)
        
        with col5:
            chart_4(year,loading_l,breadown_selection)
            
        with col6:
            chart_5(year,delivery_l,breadown_selection)
        st.write('----------------------------------------------------------------------------------------------')
        st.write('Data Table')
        
        st.header("Time Based Analysis")
        
            
        
            
        
        

    elif page == "Internal Transfer":
        st.header("Analysis of Quertransporte Data")
        st.write('This data is available at SKU level')
        st.write('Deliverer Warehouse information is given but receiver information is not present')
        st.write('There is confusion around Fabrik column,it seems to be having factory information ')
        st.write('Warehouse Id are given but Id to name mapping is not clear')
        st.write('There is another file which contains cost information for internal transfer,it has clear deliverer and receiver wh info')
        st.write('The Quertransporte file can be joined with cost data, 50 percent of Quertransporte data is matching ')
        st.write('------------------------------------------------------------------------------------------------------------------------')
    
        col_y, col_p = st.columns(2)
        with col_y:
            st.write('Year')
            options = [2022,2023,2024]
            year = st.multiselect(
                label='Select your options',
                options=options,
                default=[2022,2023,2024]  # You can set default selections here
            )
        with col_p:
            radio_options = ["Werk",'Produktgruppe','Fabrik','EME' ]
            radio_selection = st.radio("Choose an option:", radio_options)
        st.write('------------------------------------------------------------------------------------------------------------------------')    

        
        col1, col2 = st.columns(2)
        with col1:
            chart_it1(x=radio_selection,y='Menge')
        with col2:
            chart_donut_it(year,radio_selection)
        
        chart_it5(year,radio_selection)
        st.write('------------------------------------------------------------------------------------------------------------------------')
        col3, col4 = st.columns(2)
        with col3:
            chart_it3(year)
        with col4:
            chart_it4(year)
        st.write('------------------------------------------------------------------------------------------------------------------------')
        radio_options = ["Percentage","Units" ]
        percent_or_unit = st.radio("Choose an option:", radio_options)
        chart_it6(year, percent_or_unit)
        st.write('Data Table')
        st.table(df_it[:5])
        st.write('------------------------------------------------------------------------------------------------------------------------')

    elif page == "Outbound":
        
        st.header("Analysis of Sundungsdaten mit positenen Data")
        st.table(df_ob[:2])
        st.write('This data is available at SKU level')
        st.write('Deliverer Warehouse information is given but customer information is not present')
        st.write('Dispatch condition is given')
        st.write('There is another file which contains DHL shipment information,it has customer info')
        st.write('The sundungsdaten file can be joined with DHL shipment data on order id, ~99% percent of data is matching ')
        st.write('------------------------------------------------------------------------------------------------------------------------')
        
        col_y, col_p,col_d = st.columns(3)
        with col_y:
            st.write('Year')
            options = ['2022','2023','2024']
            year = st.multiselect(
                label='Select your options',
                options=options,
                default=['2022','2023','2024']  # You can set default selections here
            )
        
        radio_options = ['ShPt','SC','Produkt Typ','Material','UoM']
        radio_selection = st.radio("Choose an option:", radio_options)
        
        st.write('Total SKUs: ',df_ob['Material'].nunique())
        st.table(df_ob.groupby('year')['Number of PKT'].sum().reset_index())
        st.write('------------------------------------------------------------------------------------------------------------------------')    
        col1, col2 = st.columns(2)
        
        chart_ob1(x=radio_selection,y="Number of PKT")
        
        chart_donut_ob(year,radio_selection)
        
        radio_options_2= ["Percentage","Units"]
        percent_or_unit = st.radio("Choose an option:", radio_options_2)
        chart_ob3(year, percent_or_unit)
    
    
    
        
# Run the Streamlit app
# if st.button("Click To Run The APP"):
if __name__ == "__main__":
    main()



