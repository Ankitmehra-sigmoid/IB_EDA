
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
    .agg({'Packages':['sum','mean'],metric:['sum','mean']})
    top_field1_group.columns = top_field1_group.columns.map('_'.join)
    top_field1_group['percentage_sales']=(top_field1_group['Packages_sum']/sum(top_field1_group['Packages_sum']))*100
    top_field1_group['Rank'] = top_field1_group['percentage_sales'].rank(ascending=False)
    top_field1_group=top_field1_group.sort_values(by=['percentage_sales'],ascending=False).head(top)


    top_field1=list(top_field1_group[field1+str('_')])

    top_field2_group=data.groupby([field2], as_index=False)\
    .agg({'Packages':['sum','mean'],metric:['sum','mean']})
    top_field2_group.columns = top_field2_group.columns.map('_'.join)
    top_field2_group['percentage_sales']=(top_field2_group['Packages_sum']/sum(top_field2_group['Packages_sum']))*100
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