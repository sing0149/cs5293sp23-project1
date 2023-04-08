## cs5293sp23-Project1

## Name: Sagar Singh

## Requirements (also check requirements.txt)
attrs==22.2.0
blis==0.7.9
catalogue==2.0.8
certifi==2022.12.7
charset-normalizer==3.1.0
click==8.1.3
confection==0.0.4
cymem==2.0.7
distlib==0.3.6
en-core-web-lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.5.0/en_core_web_lg-3.5.0-py3-none-any.whl
en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0-py3-none-any.whl
filelock==3.10.7
idna==3.4
iniconfig==2.0.0
Jinja2==3.1.2
joblib==1.2.0
langcodes==3.3.0
MarkupSafe==2.1.2
murmurhash==1.0.9
nltk==3.8.1
numpy==1.24.2
packaging==23.0
pathy==0.10.1
pipenv==2023.3.20
platformdirs==3.2.0
pluggy==1.0.0
preshed==3.0.8
pydantic==1.10.7
pytest==7.2.2
regex==2023.3.23
requests==2.28.2
scikit-learn==1.2.2
scipy==1.10.1
smart-open==6.3.0
spacy==3.5.1
spacy-legacy==3.0.12
spacy-loggers==1.0.4
srsly==2.4.6
thinc==8.1.9
threadpoolctl==3.1.0
tqdm==4.65.0
typer==0.7.0
typing_extensions==4.5.0
urllib3==1.26.15
virtualenv==20.21.0
virtualenv-clone==0.5.7
wasabi==1.1.1


## Installations
Before executing ,following libraries should be installed in the environment:
argparse
nltk
os
shutil
glob
spacy
re
sklearn





## Running the Project
1. Clone the repository to local machine , or download the file in ZIP format and extract it.
2. Open terminal and navigate to the directory with the code.
3. Run the command "pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --genders --address\
                    --output 'files/' \
                    --stats stderr
"  ,,,, you cand change the flags accordingly
4. The code will redact the data and save it in the given path.
5. It will also display the stats of the files redacted, cateogary wise.


## Assumptions made before writing the code
1. The input file is in text format (e.g.,.txt,.doc, or a converted.pdf), and Python's built-in open() function can read it.
2. The input document includes Personally Identifying Information (PII), including names, contact information, addresses, dates, and terms that are specific to a certain gender.
3. To protect data privacy, the PII in the input document must be redacted.
4. Redacted placeholders such as "[NAME]", "[PHONE]", "[ADDRESS]", "[DATE]", and "[GENDER]" will be used in place of the PII by the redaction function.
5. The redaction function will produce a new, redacted version of the document rather than altering the original input document.
6. Several text forms, such as uppercase, lowercase, or mixed case, will be supported by the redaction function.
7. The redaction mechanism will be able to handle numerous PII types, including dates with varied formats, such as "MM/DD/YYYY" or "YYYY-MM-DD," and phone numbers with or without hyphens or parenthesis.
8. Instead of changing the original input document, the redaction function will create a new, redacted version of the document.
9. The redaction tool will support a variety of text formats, including mixed case, lowercase, and capital letters.
10. Many PII kinds, including as dates with different formats, such as "MM/DD/YYYY" or "YYYY-MM-DD," and phone numbers with or without hyphens or parentheses, will be supported by the redaction process.

## functions used
1. main()
This function takes in input patterns, redaction flags, output path, and statistics path as parameters. It redacts delicate data from records that match the information patterns and composes the redacted information to the output path. It likewise creates statistics on the redaction interaction and thinks of them to a statistics path. The function utilizes fundamental redaction functions, for example, redact_names, redact_dates, redact_phnumber, redact_address, and redact_genderTerms to redact delicate data. The redaction cycle and statistics age can be modified utilizing different flags. The function handles situations where there are no records matching the information example and prints a blunder message.

2. redact_phnumber():
 It instates a worldwide variable to monitor the quantity of telephone numbers redacted. It makes a spaCy Doc object, a Matcher object, and characterizes patterns to match telephone numbers. It looks for telephone number matches, affixss the matched tokens' files to a rundown, and augmentations the worldwide variable for each match.

 3. redact_names():
It acknowledges a rundown of record tokens and introduces a worldwide variable to monitor the quantity of names redacted. It emphasizes over the tokens in the info rundown and checks assuming that the symbolic's substance type is "Individual" or "Organization". On the off chance that the token matches both of these element types, it increases the worldwide variable and attaches the symbolic's beginning and end records to a rundown named terms_to_be_redacted. The rundown is utilized to monitor what parts of the text ought to be redacted.

4. redact_genderTerms():
It function redacts orientation related terms from a rundown of spaCy Doc tokens. It utilizes a predefined rundown of orientation related terms and circles over every token to check in the event that it coordinates with any of the terms. In the event that there is a match, the function augments a worldwide variable for the complete number of orientation related terms redacted and attaches the beginning and end files of the matched token to a rundown named terms_to_be_redacted.

5. redact_address():
This takes in a rundown of record tokens and looks for tokens that address locations, nations, or areas. In the event that a match is found, the function augments the total_numberof_addressesRedacted worldwide variable and adds the beginning and end records of the matched token to the terms_to_be_redacted list. The function doesn't bring anything back. The motivation behind this function is to redact any delicate data connected with addresses or areas from the information text.

6. redact_dates():
 redacts all dates found in the document_tokens via looking for tokens with the element type "DATE". It makes a rundown of start and end records for each date found, and afterward adds these files to the terms_to_be_redacted list. It likewise augments the worldwide variable total_numberof_datesRedacted by the quantity of dates found. This function can be utilized to safeguard individual data that incorporates dates, for example, birthdates or arrangement dates.

 7. redact_file():
 It takes a string as information and redacts every one of the terms present in the worldwide rundown terms_to_be_redacted by supplanting them with blocks of Unicode character \u2588. The redacted text is returned as a string. This function is helpful in situations where delicate data should be stowed away from general visibility, for example, redacting individual data from public records.

 8. remove_char():
 The remove_char function utilizes Spacy to preprocess the info text by eliminating explicit characters and tokenizing the text into individual words. It then, at that point, eliminates stop words, accentuations and spaces from the tokens and returns a rundown of the handled tokens. The function is helpful for tidying up message prior to applying NLP strategies like named element acknowledgment and opinion examination.

 9. set_output_flags():
 Function sets the output index path and sets flags to show whether the redacted text ought to be kept in touch with a record or printed to the control center. In the event that the output registry as of now exists, it is erased and reproduced. There is no such thing as in the event that the output registry, it is made. The function likewise refreshes the worldwide output_file_flag to Valid on the off chance that the output catalog isn't in the pre-characterized output_flags list.

 10. set_stats_paths():
 This function sets the path for the statistics documents to be composed to, making the catalog on the off chance that it doesn't exist as of now.

## Test Functions


1. sample_test_document(): This function peruses an example text record from a document and returns the items as a string. This function is utilized in the test functions to give an example report to testing the redaction functions.

2. test_remove_char(): This is a pytest test function that tests the remove_char() function to guarantee it accurately tokenizes and eliminates characters from the example report.

3. test_redact_phonenums(): This is a pytest test function that tests the redact_phnumber() function to guarantee it accurately redacts telephone numbers from the example record.

4. test_redact_names(): This is a pytest test function that tests the redact_names() function to guarantee it accurately redacts names from the example report.

5. test_redact_dates(): This is a pytest test function that tests the redact_dates() function to guarantee it accurately redacts dates from the example report.

6. test_redact_address(): This is a pytest test function that tests the redact_address() function to guarantee it accurately redacts addresses from the example record.

7. test_redact_genders(): This is a pytest test function that tests the redact_genderTerms() function to guarantee it accurately redacts orientation related terms from the example report.


## Bugs and Assumption

There are a few potential errors and presumptions that should be taken into account based on the functions offered:

Bugs:

1. Certain names may not be accurately identified by the redact names function, especially if they are misspelled or the NLP model being used does not recognize them.
2. All addresses might not be correctly recognized by the redact address function, especially if they are written in a non-standard format or include typos.
3. All dates might not be successfully identified by the redact dates function, especially if they are written in an unusual format or have typos.
4. The redact genderTerms function might not correctly identify every phrase with a gender or might mistakenly identify terms without a gender.

Assumptions:

1. The functions presume that the input text is in English and adheres to grammar and spelling conventions in that language.
2. The routines presuppose that the input text is correctly formatted and devoid of noise or unnecessary information.
3. The functions presumptively work with data that is written in a standard format and isn't encrypted or obfuscated.
4. The routines presuppose that any phone numbers that need to be redacted are in a normal format without any special characters or international calling codes.





## Workflow
This redaction tool's entry point is the main function main(). There are four defenses:

A list of file glob patterns to match the files to be redacted is provided as input pattern.
Redaction types to be applied to the input files are listed in redaction flags.
output path is a string that designates the location where the output files with redactions should be saved.
statistics path is a string that designates the location where the statistics files ought to be saved.

This redaction tool's process is as follows:

Based on the specified output and statistics pathways, set the output and statistics flags.
Find all the files that match the pattern for each input file pattern.
Follow these procedures for each file you find:
Get the input file's file extension.
Read the content of the input file by opening it.
The remove char() function can be used to remove any undesirable characters from the input text.
Use the matching functions from the basic redacting functions dictionary to apply the chosen redaction types to the input text.
According to the output flags set, save the redacted output to the desired location or locations.
Create statistics on the redactions made using the chosen redaction kinds, and then save them to the specified area or locations in accordance with the flags you set for statistics.
If no files matched the pattern, print a message to the terminal.

## How to run# cs5293sp23-project1
![Screen_Recording_2023-04-04_at_9_24_15_PM_AdobeExpress](https://user-images.githubusercontent.com/124123388/230703789-2bf4ca11-341d-48b5-8678-cc6e77bab252.gif)








# cs5293sp23-project1
