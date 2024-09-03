import streamlit as st
from openai import OpenAI

'''
Function requiring OpenAI API
- compare_resume:
    - main function for main.py
    - 1 resume -> 1 job description
    - compares a resume to a job description and outputs a detailed analysis of the candidate's qualifications
'''

# Load OpenAI API key
api_key = st.secrets['OPENAI_API_KEY']

@st.cache_data
def compare_resume(resume_text, jd_title, jd_text, language):
    '''

    Final HTML output version of the function
    '''

    with st.spinner('ResumeMatching...'):

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                "content": "You are a tech recruiter screening resumes."
                },
                {
                    "role": "user",
                    "content": f"""
                    Resume: ```{resume_text}```
                    Job Description: ```{jd_text}```
                    Given the above resume and job description delineated by ```, identify the skills and qualifications from both.
                    Compare them to determine any skill gaps and estimate how qualified the individual is for the job.
                    Give a percentage estimating how qualified the individual is for the job.

                    Please penalize heavily for any missing mandatory qualifications.
                    If the candidate is missing any mandatory qualifications, please also give a warning.

                    If any of the conditionsa are true, please give warnings for the ones that are true:
                    - if candidate is missing mandatory qualifications: "Candidate may be missing mandatory qualifications. Please review carefully."
                    - if resume does not mention a 4-year degree, bachelor's, master's, or PhD (or any of them in japanese), or only mentions associate's degree and/or high school diploma: "Candidate may not have university degree. Highest education listed is [highest education listed]."
                    - if candidate is outside of Japan, please give a warning: "Candidate may be overseas. Beware of hiring timelines and visa eligibility." (assume that their last place of work is their current location)
                    - if you cannot confirm candidate fulfills jd language requirements or if resume and job description are in different languages, please give a warning: "Language requirements are not confirmed. Please verify before proceeding."

                    Output format should be as below, with each section title in large font.
                    Please fill in the blanks with the appropriate information.
                    Please make sure output language is in {language}.

                    OUTPUT FORMAT:

                    <h2>Estimated Match: [percentage]</h2>

                    <ul>
                        <li>⚠️ (if mandatory qualifications are missing, give a warning here)</li>
                        <li>⚠️ (if resume does not mention a 4-year degree, bachelor's, master's, or PhD, or only mentions associate's degree and/or high school diploma, give a warning here)</li>
                        <li>⚠️ (if candidate is not in Japan, give a warning here)</li>
                        <li>⚠️ (if language requirements are not confirmed, give a warning here)</li>
                    </ul>

                    <h4>Job Description Summary:</h5>
                    <p>{jd_title}: [One sentence summary of the job description.]</p>

                    <h4>Resume Summary:</h5>
                    <ul>
                        <li>[Summary of the resume in one sentence. Please include years of experience if discernible.]</li>
                        <li><b>Current location:</b> [current location] </li>
                        <li><b>Highest eduation:</b> [highest education listed] [</li>
                        <li><b>Japanese language ability:</b> [Japanese language ability discernible from resume] </li>
                        <li><b>English language ability:</b> [English language ability discernible from resume</li>
                    </ul>

                    <h3>Comparison Analysis:</h3>
                    [reason why you gave the percentage]

                    <h4>Qualifications:</h4>
                    <ul>
                        <li>[✅/❌] [Qualification 1]: [What you can tell from the resume]</li>
                        <li>[✅/❌] [Qualification 2]: [What you can tell from the resume]</li>
                        <li>etc.</li>
                    </ul>

                    <h4>Nice-to-have:</h4>
                    <ul>
                        <li>[✅/❌] [Nice-to-have 1]: [What you can tell from the resume]</li>
                        <li>[✅/❌] [Nice-to-have 2]: [What you can tell from the resume]</li>
                        <li>etc.</li>
                    </ul>




                    """
                }
            ]
        )

        content = completion.choices[0].message.content

    return content
