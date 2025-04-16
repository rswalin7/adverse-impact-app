import streamlit as st
import pandas as pd

st.set_page_config(page_title="Adverse Impact Calculator")

st.title("📊 Adverse Impact Calculator")

# Load query params from URL
params = st.experimental_get_query_params()
default_group_col = params.get("group_col", ["gender"])[0]
default_group1 = params.get("group1", ["Female"])[0]
default_group2 = params.get("group2", ["Male"])[0]

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    demographic_columns = df.select_dtypes(include='object').columns.tolist()
    demographic_col = st.selectbox("Select a demographic column", demographic_columns, index=demographic_columns.index(default_group_col) if default_group_col in demographic_columns else 0)

    group_values = df[demographic_col].dropna().unique().tolist()

    group1 = st.selectbox("Select Group 1", group_values, index=group_values.index(default_group1) if default_group1 in group_values else 0)
    group2 = st.selectbox("Select Group 2", [g for g in group_values if g != group1], index=0)

    # Core logic
    def selection_rate(df, group_col, group_val):
        applied = df[(df[group_col] == group_val) & (df['Stage'] == 'New Application')]
        hired = df[(df[group_col] == group_val) & (df['Stage'] == 'Hired')]
        return len(hired) / len(applied) if len(applied) else 0

    def impact_ratio(rate1, rate2):
        return rate1 / rate2 if rate2 else None

    def impact_result(ratio):
        if ratio is None:
            return "⚠️ Cannot calculate (division by zero)"
        elif ratio < 0.80:
            return f"❌ Adverse Impact Detected: {ratio:.2f} < 0.80"
        else:
            return f"✅ No Adverse Impact: {ratio:.2f} ≥ 0.80"

    rate1 = selection_rate(df, demographic_col, group1)
    rate2 = selection_rate(df, demographic_col, group2)
    ratio = impact_ratio(rate1, rate2)

    st.subheader("📈 Results")
    st.markdown(f"**{group1} Selection Rate:** {rate1:.2%}")
    st.markdown(f"**{group2} Selection Rate:** {rate2:.2%}")
    st.markdown(f"**Impact Ratio (Group1 / Group2):** {ratio:.2f}" if ratio else "N/A")
    st.markdown(impact_result(ratio))