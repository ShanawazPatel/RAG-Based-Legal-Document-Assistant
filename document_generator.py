<<<<<<< HEAD
import streamlit as st
from utils import generate_document, download_document

def document_generator_page():
    st.header("📜 Legal Document Generator")
    st.write("Select a document type and provide required details.")

    doc_type = st.selectbox("Choose Document Type", ["Legal Notice", "Contract Agreement", "Affidavit"])
    user_input = st.text_area("Enter details for the document:")

    if st.button("Generate Document"):
        if user_input.strip():
            doc = generate_document(doc_type, user_input)
            st.success(f"{doc_type} generated successfully!")
            download_document(doc, f"{doc_type}.pdf", "pdf")
        else:
            st.error("Please enter details for the document.")
=======
import streamlit as st
from utils import generate_document, download_document, format_preview_text
from datetime import date

def document_generator_page():
    st.header("📜 Legal Document Generator")
    st.write("Select a document type and provide required details.")

    doc_type = st.selectbox("Choose Document Type", ["Legal Notice", "Contract Agreement", "Affidavit"])
    today = date.today().strftime("%B %d, %Y")

    if doc_type == "Legal Notice":
        st.subheader("Notice Details")
        recipient = st.text_input("Recipient Name")
        subject = st.text_input("Subject")
        details = st.text_area("Notice details")
        effective_date = st.text_input("Effective Date", value=today)

        # Single prepared-by input; court and clerk details are auto-generated
        prepared_by = st.text_input("Prepared By (Document Generator Name)", value="RAG Based Legal Document Assistant")

        # Auto-generated court/clerk defaults (not editable in the form)
        court_name = "Superior Court of Example County"
        jurisdiction = "State of Example"
        case_title = ""
        case_no = ""
        hearing_date = ""
        location = ""
        clerk_phone = "[Clerk Phone]"
        clerk_email = "[clerk@courtdomain.gov]"
        court_address = "[Court Address]"
        court_website = "[https://www.court-website.gov]"

        doc_data = {
            "recipient": recipient,
            "subject": subject,
            "details": details,
            "date": effective_date,
            "court_name": court_name,
            "jurisdiction": jurisdiction,
            "prepared_by": prepared_by,
            "case_title": case_title,
            "case_no": case_no,
            "hearing_date": hearing_date,
            "location": location,
            "clerk_phone": clerk_phone,
            "clerk_email": clerk_email,
            "court_address": court_address,
            "court_website": court_website,
        }
        required_fields = ["recipient", "subject", "details", "date"]
    elif doc_type == "Contract Agreement":
        party_one = st.text_input("Party One Name")
        party_two = st.text_input("Party Two Name")
        contract_details = st.text_area("Agreement details")
        term = st.text_input("Agreement Term")
        doc_data = {
            "party_one": party_one,
            "party_two": party_two,
            "details": contract_details,
            "term": term,
            "date": today,
        }
        required_fields = ["party_one", "party_two", "details", "term", "date"]
    else:
        deponent = st.text_input("Affiant Name")
        statement = st.text_area("Affidavit statement")
        declaration_place = st.text_input("Place of Declaration")
        doc_data = {
            "deponent": deponent,
            "statement": statement,
            "place": declaration_place,
            "date": today,
        }
        required_fields = ["deponent", "statement", "date"]

    if st.button("Generate Document"):
        missing = [key for key in required_fields if not doc_data.get(key) or not str(doc_data.get(key)).strip()]
        if not missing:
            doc = generate_document(doc_type, doc_data)
            st.success(f"{doc_type} generated successfully!")

            st.markdown("### Document Preview")
            preview_text = format_preview_text(doc_type, doc_data)
            st.text_area("Preview", preview_text, height=250)

            download_document(doc, f"{doc_type}.pdf", "pdf")
            download_document(doc, f"{doc_type}.docx", "docx")
        else:
            st.error("Please enter all required details for the document.")
>>>>>>> 778ca0525845585a232748686960a92a35626e59
