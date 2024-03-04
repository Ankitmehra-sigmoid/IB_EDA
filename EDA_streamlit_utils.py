
import pandas as pd
import numpy as np
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px


def normalize_and_deduplicate(column):
    normalized = column.str.upper()
    deduped = defaultdict(list)
    for name in normalized:
        core_name = name.split(',')[0].strip()
        deduped[core_name].append(name)
    name_mapping = {variation: core for core, variations in deduped.items() for variation in variations}
    standardized_column = column.map(name_mapping).fillna(column)
    return standardized_column

def standerdize_cols(df,selected_cols):

    # Apply the function to all non-numeric columns
    for column in selected_cols:
        print(column)
        df[column]=df[column].fillna('Missing')
        if df[column].dtype == 'object':  # Check if the column is non-numeric
            df[column] = normalize_and_deduplicate(df[column])
    return df

def top_five(df,column):
    a=df.groupby([column])['Packages'].sum().reset_index()
    a=a.sort_values(by=['Packages'],ascending=False)
    return list(a[column][:5])
    
def grouping(df,group_by_1,group_by_2,target_col):
   
    grouped_df=df.groupby([group_by_1,group_by_2])[target_col].sum().reset_index()
    
        

    grouped_sum =  grouped_df.groupby(group_by_1)[target_col].transform('sum')

    # Calculate the percentage of each 'Number' relative to the group sum
    grouped_df['Percentage'] = (grouped_df[target_col] / grouped_sum) * 100

    # Check the result
    return grouped_df

def plot_warehouse_yearly_quantity_3(df,x, y, breakdown_col, df_in, is_percent,title):
    
    # df = df[df[x].isin(top_five(df=df_in, column=x))]
    # Pivot the data to prepare for stacked bar chart
    pivot_df = df.pivot_table(index=x, columns=breakdown_col, values=y, fill_value=0)

    # Create a bar for each breakdown category
    bars = []
    for breakdown_col in pivot_df.columns:
        if is_percent:
            # When is_percent is True, format the text with a percentage sign
            bar_text = pivot_df[breakdown_col].apply(lambda x: f'{x:.2f}%')
        else:
            # Otherwise, just round the values
            bar_text = round(pivot_df[breakdown_col], 4)
        if is_percent:
            bars.append(go.Bar(
            name=breakdown_col,
            x=pivot_df.index,
            y=pivot_df[breakdown_col],
            text=bar_text,
            textposition='outside'))
        else:
            bars.append(go.Bar(
            name=breakdown_col,
            x=pivot_df.index,
            y=pivot_df[breakdown_col],
            # text=bar_text,
            textposition='outside'))
        
        

    # Create a figure
    fig = go.Figure(data=bars)

    # Update the layout to stack the bars
    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis=dict(title=x),
        yaxis=dict(title=y),
        uniformtext_minsize=8,  # Ensures text fits even in small segments
        uniformtext_mode='hide'  # Hides text if it doesn't fit
    )

    bar_width = 0.5  # Adjust this value to change the width of the bars
    fig.update_traces(width=bar_width)

    # if is_percent:
#         # Format the y-axis tick labels as percentages
        # fig.update_yaxes(tickformat=".2%")
        # Format the bar text labels as percentages (already done in the loop above)

    # Show the figure
    # fig.show()
    st.plotly_chart(fig)

def plot_bar(data,field,metric,aggrigation,top,percent=False):
    
    if percent:
        metric_sum=metric+str('_sum')
        metric_per=metric+str('_percentage')
        metric_mean=metric+str('_mean')
        grouped_data = data.groupby([field], as_index=False)\
        .agg({metric:['sum','mean']})
        
        grouped_data.columns = grouped_data.columns.map('_'.join)
        grouped_data[metric_per]=((grouped_data[metric_sum]/sum(grouped_data[metric_sum])))
        grouped_data[metric_mean]=((grouped_data[metric_mean])).round(2)  
    else:
        metric_sum=metric+str('_sum')
        metric_per=metric+str('_percentage')
        metric_mean=metric+str('_mean')
        grouped_data = data.groupby([field], as_index=False)\
        .agg({metric:['sum','mean']})
        grouped_data.columns = grouped_data.columns.map('_'.join)
        grouped_data[metric_per]=((grouped_data[metric_sum]/sum(grouped_data[metric_sum])))
        grouped_data[metric_mean]=((grouped_data[metric_mean])).round(4)
    
    if(percent):
        ranking_column=metric_per
    else:
        ranking_column=metric+str('_')+aggrigation
    xx=field+str('_')
    # grouped_data=grouped_data.sort_values(by=[ranking_column],ascending=False).head(top)
    grouped_data=grouped_data.sort_values(by=[ranking_column],ascending=False)
    fig = px.bar(grouped_data, x=xx, y=ranking_column, color=xx,
                 color_discrete_sequence=['#FF0000','#8B0000','#666666','#999999','#C0C0C0'],
                 text_auto=True,
                title='Profile of Inbound for Top 5 '+ field +' ' ,
                labels={xx:field,ranking_column:metric})
    #fig.update_layout(template= 'pltly_white')
    if(percent):
        fig.update_yaxes(tickformat=".2%")
    st.plotly_chart(fig)

def plot_heatmap_percent(percent_inbound,field1,field2,fig_width=900):
    heatmap_data = percent_inbound.iloc[:, 1:]
    # Create the heatmap figure using only the cell values
    #col_to_use=['DREIEICH','KREFELD','LANGENHAGEN','MEERANE','SCHWIEBERDINGEN']
    col_to_use=list(percent_inbound.columns)[1:]
    
    fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=heatmap_data.columns,
            y=percent_inbound[field1],
            text=percent_inbound[col_to_use].astype(str),
            texttemplate="%{text}%",
            xgap=5,
            ygap=5,
            colorscale=[[0, 'grey'], [1, 'red']],
            colorbar=dict(
    #             tickvals=[0, 0.5, 1],
    #             ticktext=['0%', '50%', '100%'],
    #             tickmode='array',
                x=1.07,
                len=1,
                outlinewidth=0,
                thickness=20
            )
        ))

    # Annotate the heatmap with row and column totals (excluding the last row and last column)
    for i, row_total in enumerate(percent_inbound.iloc[:, 1:].sum(axis=1)):
        fig.add_annotation(text=f'{row_total:.2f}%', xref='paper', yref='y', x=1.08, y=i, showarrow=False)
    for j, col_total in enumerate(percent_inbound.iloc[:, 1:].sum()):
        fig.add_annotation(text=f'{col_total:.2f}%', xref='x', yref='paper', x=j, y=1.1, showarrow=False)

    # Customize the layout
    fig.update_layout(
        title='Profile between ' +field1+' and ' +  field2,
        template='plotly_white',
        xaxis=dict(ticks='', nticks=len(percent_inbound.columns)),
        yaxis=dict(ticks='', nticks=len(percent_inbound[field1])),  # Adjust the number of y-axis ticks to exclude the last row
        xaxis_title=field2,
        yaxis_title=field1,
        width=fig_width


    #     margin=dict(l=25, r=25, b=25, t=25)
    )

    # fig.update_traces(coloraxis_colorbar=dict(thickness=20, len=0.75))

    # Show the plot
    st.plotly_chart(fig)

def plot_heatmap_normal(percent_inbound,field1,field2,aggrigation,fig_width=900):
    heatmap_data = percent_inbound.iloc[:, 1:]
    # Create the heatmap figure using only the cell values
    #col_to_use=['DREIEICH','KREFELD','LANGENHAGEN','MEERANE','SCHWIEBERDINGEN']
    col_to_use=list(percent_inbound.columns)[1:]
    fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=heatmap_data.columns,
            y=percent_inbound[field1],
            text=percent_inbound[col_to_use].astype(str),
            texttemplate="%{text}",
            xgap=5,
            ygap=5,
            colorscale=[[0, 'grey'], [1, 'red']],
            colorbar=dict(
    #             tickvals=[0, 0.5, 1],
    #             ticktext=['0%', '50%', '100%'],
    #             tickmode='array',
                x=1.07,
                len=1,
                outlinewidth=0,
                thickness=20
            )
        ))
    if(aggrigation=='sum'):
        # Annotate the heatmap with row and column totals (excluding the last row and last column)
        for i, row_total in enumerate(percent_inbound.iloc[:, 1:].sum(axis=1)):
            fig.add_annotation(text=f'{row_total:.2f}', xref='paper', yref='y', x=1.08, y=i, showarrow=False)
        for j, col_total in enumerate(percent_inbound.iloc[:, 1:].sum()):
            fig.add_annotation(text=f'{col_total:.2f}', xref='x', yref='paper', x=j, y=1.1, showarrow=False)
    else:
        # Annotate the heatmap with row and column totals (excluding the last row and last column)
        for i, row_total in enumerate(percent_inbound.iloc[:, 1:].mean(axis=1)):
            fig.add_annotation(text=f'{row_total:.2f}', xref='paper', yref='y', x=1.08, y=i, showarrow=False)
        for j, col_total in enumerate(percent_inbound.iloc[:, 1:].mean()):
            fig.add_annotation(text=f'{col_total:.2f}', xref='x', yref='paper', x=j, y=1.1, showarrow=False)       

    # Customize the layout
    fig.update_layout(
        title='Profile between ' +field1+' and ' +  field2,
        template='plotly_white',
        xaxis=dict(ticks='', nticks=len(percent_inbound.columns)),
        yaxis=dict(ticks='', nticks=len(percent_inbound[field1])),  # Adjust the number of y-axis ticks to exclude the last row
        xaxis_title=field2,
        yaxis_title=field1,
        width=fig_width


    #     margin=dict(l=25, r=25, b=25, t=25)
    )

    # fig.update_traces(coloraxis_colorbar=dict(thickness=20, len=0.75))

    # Show the plot
    st.plotly_chart(fig)

def plot_heatmap(data,field1,field2,metric,aggrigation,top,percent=False):
    
    if percent:
        metric_sum=metric+str('_sum')
        metric_per=metric+str('_percentage')
        metric_mean=metric+str('_mean')
        grouped_data = data.groupby([field1,field2], as_index=False)\
        .agg({metric:['sum','mean']})
        
        grouped_data.columns = grouped_data.columns.map('_'.join)
        grouped_data[metric_per]=((grouped_data[metric_sum]/sum(grouped_data[metric_sum]))*100).round(2)
        grouped_data[metric_mean]=((grouped_data[metric_mean])).round(2)  
    else:
        metric_sum=metric+str('_sum')
        metric_per=metric+str('_percentage')
        metric_mean=metric+str('_mean')
        grouped_data = data.groupby([field1,field2], as_index=False)\
        .agg({metric:['sum','mean']})
        grouped_data.columns = grouped_data.columns.map('_'.join)
        grouped_data[metric_per]=((grouped_data[metric_sum]/sum(grouped_data[metric_sum]))*100).round(2)
        grouped_data[metric_mean]=((grouped_data[metric_mean])).round(2)
                             
    #print(grouped_data.head())
    top_field1_group=data.groupby([field1], as_index=False)\
    .agg({metric:['sum','mean'],metric:['sum','mean']})
    top_field1_group.columns = top_field1_group.columns.map('_'.join)
    top_field1_group['percentage_sales']=(top_field1_group[metric+'_sum']/sum(top_field1_group[metric+'_sum']))*100
    top_field1_group['Rank'] = top_field1_group['percentage_sales'].rank(ascending=False)
    top_field1_group=top_field1_group.sort_values(by=['percentage_sales'],ascending=False).head(top)


    top_field1=list(top_field1_group[field1+str('_')])

    top_field2_group=data.groupby([field2], as_index=False)\
    .agg({metric:['sum','mean'],metric:['sum','mean']})
    top_field2_group.columns = top_field2_group.columns.map('_'.join)
    top_field2_group['percentage_sales']=(top_field2_group[metric+'_sum']/sum(top_field2_group[metric+'_sum']))*100
    top_field2_group['Rank'] = top_field2_group['percentage_sales'].rank(ascending=False)
    # top_field2_group=top_field2_group.sort_values(by=['percentage_sales'],ascending=False).head(top)
    top_field2_group=top_field2_group.sort_values(by=['percentage_sales'],ascending=False)

    top_field2=list(top_field2_group[field2+str('_')])


    grouped_data=grouped_data[grouped_data[field1+str('_')].isin(top_field1)]
    grouped_data=grouped_data[grouped_data[field2+str('_')].isin(top_field2)]

    metric_use=metric+str('_')+aggrigation
    field1_use=field1+str('_')
    field2_use=field2+str('_')


    if(percent):
        metric_use=metric_per

    col_to_use1 = metric_use
    pivot_final_data = grouped_data.pivot(
    index=[field1_use],
    columns=[field2_use],
    values=[col_to_use1]
    ).reset_index()
    pivot_final_data.rename(columns = {metric_use:''}, inplace = True) 
    pivot_final_data.rename(columns = {field1_use:field1}, inplace = True) 
    pivot_final_data.columns = pivot_final_data.columns.map(''.join)
    percent_inbound=pivot_final_data

    percent_inbound['rank2']= percent_inbound.iloc[:, 1:].sum(axis=1)

    percent_inbound = percent_inbound.iloc[:, :-1]
    #print(percent_inbound)
    custom_order=list(percent_inbound[field1])
    percent_inbound[field1]=pd.Categorical(percent_inbound[field1], categories=custom_order, ordered=True)
    percent_inbound = percent_inbound.sort_values(by=field1)
    #print(percent_inbound.head())

    if(percent):
        plot_heatmap_percent(percent_inbound,field1,field2)
    else:
        plot_heatmap_normal(percent_inbound,field1,field2,aggrigation)

def format_integer(value):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.2f}M'
    elif value >= 1_000:
        return f'{value / 1_000:.2f}K'
    else:
        return f'{value}'


def monthly_distribution(cc,metric,percentage,gr_title):
    # Create the stacked bar plot using Plotly Expres
    df_packages_by_month=cc.groupby(['month'])[metric].sum().to_frame().reset_index()
    df_packages_by_month[metric+str('_per')]=((df_packages_by_month[metric]/df_packages_by_month[metric].sum()))*100
    color_palette=px.colors.sequential.Reds
    if(percentage):
        text_labels = df_packages_by_month[metric+str('_per')].round(2).astype(str) + '%'
        fig = px.bar(df_packages_by_month, x='month', y=metric+str('_per'), color=metric+str('_per'),
                     title=gr_title,
                     labels={'Month': 'Month', metric+str('_per'): metric+str(' %')},
                     text=text_labels,  # Specify the text labels for the bars
                     category_orders={'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']},
                     color_discrete_sequence=color_palette)
#         fig.update_layout(template= 'plotly_white')
        #fig.update_yaxes(tickformat=".2%")
        fig.show()
    else:
        # Apply the formatting function to each value in the metric column
        text_labels = df_packages_by_month[metric].apply(format_integer)
        fig = px.bar(df_packages_by_month, x='month', y=metric, color=metric,
                     title=gr_title,
                     labels={'Month': 'Month', metric: metric},
                     text=text_labels,  # Specify the text labels for the bars
                     category_orders={'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']},
                     color_discrete_sequence=color_palette)
        fig.update_layout(template= 'plotly_white',yaxis_tickformat=',.0f',width=900)
        #fig.update_yaxes(tickformat=".2%")
        st.plotly_chart(fig)

def side_by_side_bar(df,x,y,breakdown_by,gr_title):
    df = df.groupby([x,breakdown_by], as_index=False)[y].sum().sort_values(by=[breakdown_by,y], ascending=[True,False])

    df[breakdown_by]=df[breakdown_by].astype('str')
    fig = px.bar(
        df ,
        x=x,
        y=y,
        color=breakdown_by,  # Differentiate bars by year using color
        title=gr_title,
        barmode='group'  # Set barmode to 'group' for side-by-side bars
    )

    # Update layout if necessary
    fig.update_layout(
        yaxis=dict(title=y),
        xaxis=dict(title=x),
        width=950
    )

    # Show the figure
    st.plotly_chart(fig)

def plot_donut(data,field2,metric):
    
        
    df_packages_by_delivery_product=data.groupby([field2])[metric].sum().to_frame().reset_index()
    df_packages_by_delivery_product[metric+str('_per')]=((df_packages_by_delivery_product[metric]/df_packages_by_delivery_product[metric].sum()))
    
    ## top 5 product groups
    
    # Get the top 5 most frequent values in the column
    # Group the data by category and calculate total sales
    category_sales = df_packages_by_delivery_product.groupby(field2)[metric].sum()

    # Sort the categories based on sales in descending order
    sorted_category_sales = category_sales.sort_values(ascending=False)

    # Select the top 5 categories
    #top_5_categories = sorted_category_sales.head(5)
    top_values= sorted_category_sales.head(5)
    # Replace values not in the top 5 with 'Others'
    df_packages_by_delivery_product[field2] = df_packages_by_delivery_product[field2].apply(lambda x: x if x in top_values else 'Others')
    
    
    fig = px.pie(df_packages_by_delivery_product, values=metric, names=field2,
             title='',
             labels={field2:field2,metric:metric},
            hole=0.5)

    fig.update_traces(textinfo='percent+label')

    fig.update_layout(template= 'plotly_white')
    st.plotly_chart(fig)

def create_line_graph(df, time_col, packages_col, category_col):
    """
    Creates a line graph with the specified columns.

    Parameters:
    - df: pandas.DataFrame containing the data
    - time_col: the name of the column to be used as the x-axis (time)
    - packages_col: the name of the column to be used as the y-axis (packages)
    - category_col: the name of the column to break down the lines by category

    Returns:
    - fig: Plotly figure object
    """
    # Create the line chart using Plotly Express
    fig = px.line(
        df,
        x=time_col,
        y=packages_col,
        color=category_col,  # Different lines for each category
        title=f'Packages Over Time by {category_col}'
    )
    
    # Update layout for better readability if necessary
    fig.update_layout(
        xaxis_title=time_col,
        yaxis_title=packages_col,
        legend_title=category_col,
        width=950 )
    
    # Show the figure
    st.plotly_chart(fig)
    
    
