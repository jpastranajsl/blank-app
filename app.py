import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO

# Title and Description
st.title("📊 Automated Financial Report Generator")
st.write("Upload your financial CSV file to generate a professional PDF report.")

# Business Info Form (Sidebar)
st.sidebar.header("🏢 Business Information")
business_name = st.sidebar.text_input("Business Name")
owner_name = st.sidebar.text_input("Owner Name")
business_address = st.sidebar.text_area("Business Address")
reporting_month = st.sidebar.selectbox("Reporting Month",
                                       ["January", "February", "March", "April", "May", "June",
                                        "July", "August", "September", "October", "November", "December"])
additional_notes = st.sidebar.text_area("Additional Notes")

# Logo Upload
st.sidebar.header("🖼️ Upload Business Logo (Optional)")
uploaded_logo = st.sidebar.file_uploader("Upload a PNG or JPG file", type=["png", "jpg", "jpeg"])

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
	st.success("✅ File uploaded successfully!")

    # Read the CSV into a DataFrame
	df = pd.read_csv(uploaded_file)

    # Convert Date column to datetime format
	df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    # Clean the Amount column (remove $ and commas)
	df["Amount"] = df["Amount"].astype(str).str.replace("[ Kč]", "", regex=True).str.replace(",", ".")
	df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

	#Strip spaces from category names (fixes extra spaces)
	df["Category"] = df["Category"].astype(str).str.strip()

	print(df.head())

    # Compute Totals
	total_revenue = df[df["Type"] == "Revenue"]["Amount"].sum()
	total_expenses = df[df["Type"] == "Expense"]["Amount"].sum()
	net_profit = total_revenue - total_expenses
	profit_margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0

    # Generate Charts
	def create_chart(fig):
		buf = BytesIO()
		fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
		buf.seek(0)
		return buf

    # Revenue vs. Expenses Chart
	fig, ax = plt.subplots()
	ax.bar(["Revenue", "Expenses"], [total_revenue, total_expenses], color=["green", "red"])
	ax.set_title("Revenue vs. Expenses")
	rev_exp_chart = create_chart(fig)

    # Profit Trend Chart
	fig, ax = plt.subplots()
	monthly_profit = df.groupby(df["Date"].dt.month)["Amount"].sum()
	ax.plot(monthly_profit.index, monthly_profit.values, marker="o", linestyle="-", color="blue")
	ax.set_title("Profit Trend Over Time")
	profit_trend_chart = create_chart(fig)

# Function to Create Pie Chart with a Side Legend
	def create_pie_chart_with_side_legend(data, title):
		fig, ax = plt.subplots(figsize=(10, 6))  # Wider figure to fit legend on the side

		# Generate pie chart (NO labels inside)
		wedges, texts = ax.pie(data, colors=plt.cm.Paired.colors, startangle=140)

		if not plt.gcf().get_axes()[0].texts:  # Only add title if it's not already set
			ax.set_title(title, fontsize=16, fontweight="bold")

		# Create LEGEND on the RIGHT side
		legend_labels = [f"{category}: ${amount:,.2f}" for category, amount in data.items()]
		ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12, frameon=False)

		buf = BytesIO()
		fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")  # Save full chart including legend
		buf.seek(0)
		return buf

	# Revenue Breakdown Pie Chart
	revenue_by_category = df[df["Type"] == "Revenue"].groupby("Category")["Amount"].sum()
	revenue_chart = create_pie_chart_with_side_legend(revenue_by_category, "Revenue Breakdown")

	# Expense Breakdown Pie Chart
	expenses_by_category = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()
	expense_chart = create_pie_chart_with_side_legend(expenses_by_category, "Expense Breakdown")


    # Generate PDF
	def generate_pdf():
		buffer = BytesIO()
		pdf = canvas.Canvas(buffer, pagesize=letter)
		width, height = letter

		# Page 1: Minimalist Cover Page
		pdf.setFont("Helvetica-Bold", 36)
		pdf.drawCentredString(width / 2, height - 100, "Financial Report")

		# Separation Line
		pdf.setStrokeColor(colors.black)
		pdf.setLineWidth(1.5)
		pdf.line(50, height - 120, width - 50, height - 120)

		# Centered Business Information
		pdf.setFont("Helvetica", 14)
		pdf.drawCentredString(width / 2, height - 180, f"{business_name}")
		pdf.drawCentredString(width / 2, height - 210, f"{owner_name}")
		pdf.drawCentredString(width / 2, height - 240, f"{business_address}")
		pdf.drawCentredString(width / 2, height - 270, f"Reporting Month: {reporting_month}")

		# Centered Logo (if provided)
		if uploaded_logo:
			logo = ImageReader(uploaded_logo)
			logo_width = 120
			logo_height = 120
			pdf.drawImage(logo, (width - logo_width) / 2, height - 400, width=logo_width, height=logo_height, mask="auto")

		pdf.showPage()

		# Page 2: Executive Summary
		pdf.setFont("Helvetica-Bold", 18)
		pdf.drawString(50, height - 50, "Executive Summary")

		pdf.setFont("Helvetica", 12)
		financial_data = [
			["Total Revenue", f"${total_revenue:,.2f}"],
			["Total Expenses", f"${total_expenses:,.2f}"],
			["Net Profit", f"${net_profit:,.2f}"],
			["Profit Margin", f"{profit_margin:.2f}%"]
		]

		table = Table(financial_data, colWidths=[250, 150])
		table.setStyle(TableStyle([
			('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # Header color
			('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text for headers
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
			('FONTSIZE', (0, 0), (-1, -1), 12),
			('BOTTOMPADDING', (0, 0), (-1, -1), 6),
			('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Alternating row color
			('GRID', (0, 0), (-1, -1), 1, colors.grey)
		]))

		table.wrapOn(pdf, width, height)
		table.drawOn(pdf, 50, height - 200)

		pdf.showPage()

		pdf.setFont("Helvetica-Bold", 18)
		pdf.drawString(50, height - 50, "Revenue & Expense Breakdown")

		if rev_exp_chart:
			pdf.drawImage(ImageReader(rev_exp_chart), 50, height - 350, width=450, height=280)
		if profit_trend_chart:
			pdf.drawImage(ImageReader(profit_trend_chart), 50, height - 650, width=450, height=280)

		pdf.showPage()

		# Page 3: Revenue Breakdown
		pdf.setFont("Helvetica-Bold", 18)
		pdf.drawString(50, height - 50, "Revenue Breakdown")
		if revenue_chart:
			pdf.drawImage(ImageReader(revenue_chart), 50, height - 400, width=400, height=250)

		pdf.showPage()

		# Page 4: Expense Breakdown
		pdf.setFont("Helvetica-Bold", 18)
		pdf.drawString(50, height - 50, "Expense Breakdown")
		if expense_chart:
			pdf.drawImage(ImageReader(expense_chart), 50, height - 400, width=400, height=250)
		pdf.showPage()

		# Page 5: Profit & Loss Statement
		pdf.setFont("Helvetica-Bold", 18)
		pdf.drawString(50, height - 50, "Profit & Loss Statement")

		table.wrapOn(pdf, width, height)
		table.drawOn(pdf, 50, height - 150)

		pdf.save()
		buffer.seek(0)
		return buffer

	if st.button("📄 Generate PDF Report"):
		pdf_data = generate_pdf()
		st.download_button("📥 Download PDF", pdf_data, "Financial_Report.pdf", "application/pdf")
