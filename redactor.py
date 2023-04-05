import argparse
import glob
import nltk
import os
import spacy
import shutil
from sys import stderr, stdout
from spacy.matcher import Matcher
stdout_output_flag = False
stderr_output_flag = False
output_file_flag = False

stdout_statistics_flag = False
stderr_statistics_flag = False
statistics_file_flag = False


##########################################################################################################

output_flags={
       "stderr": stderr_output_flag,
       "stdout": stdout_output_flag,
    }

statistics_flags = {
            "stderr": stderr_statistics_flag,
            "stdout": stdout_statistics_flag   
     }



#############################################################################################################
#loading the spacy NLP pipeline
nlp= spacy.load("en_core_web_sm")

total_numberof_namesRedacted = 0
total_numberof_datesRedacted = 0
total_numberof_phoneNumRedacted = 0
total_numberof_genderTermsRedacted = 0
total_numberof_addressesRedacted= 0
terms_to_be_redacted = []


##########################################################################################################

###function to redact phone numbers using the entire processed   "file data"
def redact_phnumber(file_data):
     global total_numberof_phoneNumRedacted
     document=nlp(file_data)
     matcherObject=Matcher(nlp.vocab) 
    
     possible_phonenumber_patterns = [
     {"IS_DIGIT": True, "LENGTH": 3},  # expression for matching a three digit area code
     {"TEXT": {"IN": ["-", ".", " "]}, "OP": "?"},  # expression for matching  any  separator character like dash, dot or space)
     {"IS_DIGIT": True, "LENGTH": 3},  # this expression matches the next three digits
     {"TEXT": {"IN": ["-", ".", " "]}, "OP": "?"},  # again the expression for matching  any  separator character like dash, dot or space)
     {"IS_DIGIT": True, "LENGTH": 4}  # expression to match the last four digits of a phone number 
    ]
     matcherObject.add("Phonenum_pattern1", [possible_phonenumber_patterns])
     phonenumber_matches = matcherObject(document)
     for phonenum_matching_identity, match_start, match_end in phonenumber_matches:
        for phonematch in range(match_start, match_end):
           terms_to_be_redacted.append((document[phonematch].idx, document[phonematch].idx+len(document[phonematch].text)))
        total_numberof_phoneNumRedacted +=1

###############################################################################################################
     

#function to redact names using the document_tokens created 
def redact_names(document_tokens):
    global total_numberof_namesRedacted
    for doc_token in document_tokens:
         if doc_token.ent_type_ in {"PERSON","ORG"}:
              total_numberof_namesRedacted+=1
              terms_to_be_redacted.append((doc_token.idx,doc_token.idx + len(doc_token.text)))

 

 
 ##############################################################################################################
 
 #function to redact genders using the document_tokens created   
def redact_genderTerms(document_tokens):
    global total_numberof_genderTermsRedacted
    all_possible_gender_terms= [
    "man",
    "woman",
    "male",
    "female",
    "boy",
    "girl",
    "masculine",
    "feminine",
    "transgender",
    "cisgender",
    "nonbinary",
    "genderqueer",
    "agender",
    "bigender",
    "androgyne",
    "intersex",
    "two-spirit",
    "genderfluid",
    "demigender",
    "neutrois",
    "pangender",
    "third gender",
    "transmasculine",
    "transfeminine",
    "trans man",
    "trans woman",
    "MTF",
    "FTM",
    "enby",
    "butch",
    "femme",
    "androgynous",
    "cis man",
    "cis woman",
    "gender nonconforming",
    "gender variant",
    "gender questioning",
    "gender diverse",
    "gender expansive",
    "gender creative",
    "gender gifted",
    "gender fluidity",
    "gender identity",
    "gender expression",
    "gender roles",
    "gender stereotypes",
    "gender norms",
    "gender equality",
    "gender equity",
    "gender justice",
    "gender liberation",
    "he",    "him",    "his",    "she",    "her",   
    "hers",    "they",    "them",    "theirs",    "ze",  
    "zir",    "xe",    "xem",    "xyr",    "ey",    "em",   
    "eir",    "per",    "thon",    "ve",    "ver",    "xe",    
    "hir",    "sie",    "hirself",    "sieself",    "sie",  
    "hir",    "emself",    "perself",    "himself",    "herself", 
    "themselves",    "ze/hir",    "zie",    "zieself",    "ze/zir",   
    "xe/xem",    "xyrself",    "ey/em",    "eirself",    "ve/ver",   
    "sie/hir",    "sie/em",    "sie/eir",
    ]

    for gender_token in document_tokens:
        if gender_token.text.lower() in all_possible_gender_terms:
            total_numberof_genderTermsRedacted += 1
            terms_to_be_redacted.append((gender_token.idx, gender_token.idx+len(gender_token.text)))



#########################################################################################

## #function to add indexes of address in the given list 
def redact_address(document_tokens):
    global total_numberof_addressesRedacted
    for address_token in document_tokens:
        if address_token.ent_type_ in ["GPE" or "LOC"] or address_token.ent_type_ == "ADDRESS":
            total_numberof_addressesRedacted+= 1
            terms_to_be_redacted.append((address_token.idx, address_token.idx+len(address_token.text)))

#########################################################################################            

            
def redact_dates(document_tokens):
     global total_numberof_datesRedacted
     date_indexes= [(doc_token.idx,doc_token.idx+len(doc_token.text)) for doc_token in document_tokens if doc_token.ent_type_=="DATE"]
     terms_to_be_redacted.extend(date_indexes)
     total_numberof_datesRedacted+=len(date_indexes)


#########################################################################################                


def redact_file(file_data):
    for start_index, end_index in terms_to_be_redacted:
        term_pattern = file_data[start_index:end_index]
        redaction = "\u2588" * len(term_pattern)
        file_data = file_data[:start_index] + redaction + file_data[end_index:]

    final_redacted_text = file_data
    return final_redacted_text 

#########################################################################################

def remove_char(file_data):
     nlp=spacy.load("en_core_web_sm")
     tags=set(["<",">","=","(",")","\\","\/"])
     processed_lines="".join([char if char not in tags else " " for char in file_data])
     document=nlp(processed_lines)
     final_processed_tokens=[
          token 
          for token in document
          if not(token.is_stop or token.is_punct or token.is_space)
        ]
     return final_processed_tokens

#########################################################################################

def set_output_flags(output_directory):
    output_path_of_redacted_files=output_directory.strip("'") 
    if output_path_of_redacted_files in output_flags:
       output_flags[output_path_of_redacted_files]=True
    else:
       global output_file_flag
       output_file_flag = True
       if os.path.exists(output_path_of_redacted_files):
           shutil.rmtree(output_path_of_redacted_files)
           os.makedirs(output_path_of_redacted_files)
       else :
           os.makedirs(output_path_of_redacted_files)
    
#########################################################################################

def set_stats_paths(statistics_directory):
    output_path_of_statistics_files = statistics_directory.strip("'")
  
    if output_path_of_statistics_files in statistics_flags:
          statistics_flags[output_path_of_statistics_files]=True
    else:
       global statistics_file_flag 
       statistics_file_flag=True 
       if os.path.exists(output_path_of_statistics_files):
           shutil.rmtree(output_path_of_statistics_files)
           os.makedirs(output_path_of_statistics_files)
       else:
           os.makedirs(output_path_of_statistics_files)

      


###############    MAIN FUNCTION   #################################################################################################################

def main(
       input_pattern,
       redaction_flags,
       output_path,
       statistics_path,
):
   global terms_to_be_redacted
   global output_file_flag
   global statistics_file_flag
   set_output_flags(output_path)
   set_stats_paths(statistics_path)
   for pattern in input_pattern:
       files_toBe_redacted = glob.glob(pattern.strip("'"),recursive=True)
       if len(files_toBe_redacted)!=0:
          for file_path in files_toBe_redacted:
            file_extension=os.path.splitext(os.path.basename(file_path))[1]
                          
            with open(file_path,"r") as inputfile:
                file_data = inputfile.read()
                p_tokens= remove_char(file_data)
                basic_redacting_functions={
                       "names" : redact_names,
                       "dates": redact_dates,
                       "phones":redact_phnumber,
                       "address":redact_address,
                       "genders":redact_genderTerms,
                }
                for flag in redaction_flags:
                    if flag in basic_redacting_functions:
                        basic_redacting_functions[flag]( file_data if flag=="phones" else p_tokens)
                
                redacted_processed_data = redact_file(file_data)
                if output_flags["stdout"] == True:
                    print(f" -- Final output for {file_path}--")
                    print()
                    stdout.write(redacted_processed_data)
                if  output_flags["stderr"]==True:
                    stderr.write(redacted_processed_data)
                if output_file_flag==True:
                    redacted_file_name= (
                        os.path.splitext(os.path.basename(inputfile.name))[0]
                        +file_extension+ ".redacted"
                    )
                    with open(os.path.join(output_path_of_redacted_files, redacted_file_name), "w", encoding="utf-8") as redacted_file:
                      redacted_file.write(redacted_processed_data)

                    
                terms_to_be_redacted=[]
                # print(statistics_file_flag)
                if statistics_flags["stdout"]==True:
                     global total_numberof_namesRedacted
                     global total_numberof_datesRedacted
                     global total_numberof_phoneNumRedacted
                     global total_numberof_genderTermsRedacted
                     global total_numberof_addressesRedacted
                     string= (   f"---------Stats for {file_path} ----------\n"
                                 f"Number of names redacted from the input file are : {total_numberof_namesRedacted}\n"
                                 f"Number of dates redacted from the input file are: {total_numberof_datesRedacted}\n"
                                 f"Number of Phonenumbers redacted from the input file are: {total_numberof_phoneNumRedacted}\n"
                                 f"Number of gender terms redacted from the input file are: {total_numberof_genderTermsRedacted}\n"
                                 f"Number of addresses redacted from the input file are : {total_numberof_addressesRedacted}\n"
                            )
                     print(string)
                     total_numberof_namesRedacted = 0
                     total_numberof_datesRedacted = 0
                     total_numberof_phoneNumRedacted = 0
                     total_numberof_genderTermsRedacted = 0
                     total_numberof_addressesRedacted= 0
                if statistics_flags["stderr"] == True:
                            stderr.write("Redaction Successfull ! ")
                            statisitics_results = "".join(
                                    [
                                        f"---------Stats for {file_path} --------------",
                                        "\n",
                                        f"Number of names redacted from the input file: {total_numberof_namesRedacted}",
                                        "\n",
                                        f"Number of dates redacted from the input file: {total_numberof_datesRedacted}",
                                        "\n",
                                        f"Number of Phone numbers redacted from the input file: {total_numberof_phoneNumRedacted}",
                                        "\n",
                                        f"Number of gender terms redacted from the input file: {total_numberof_genderTermsRedacted}", 
                                        "\n",
                                        f"Number of addresses redacted from the input file: {total_numberof_addressesRedacted}", 
                                        "\n",
                                    ]
                                )
                           
                            stderr.write(statisitics_results)
                if statistics_file_flag == True:
                            stats_file_name = (os.path.splitext(os.path.basename(inputfile.name))[0]+ "-stats.txt")
                            with open("".join([statistics_display_place, stats_file_name]),"w",encoding="utf-8",) as stat_file:
                               statisitics_results = "".join(
                                    [
                                        f"----Statistics for {file_path} -------",
                                        "\n",
                                        f"Names redacted: {total_numberof_namesRedacted}",
                                        "\n",
                                        f" Dates redacted: {total_numberof_datesRedacted}",
                                        "\n",
                                        f"Phone numbers redacted: {total_numberof_phoneNumRedacted}",
                                        "\n",
                                        f"Gender terms redacted: {total_numberof_genderTermsRedacted}", 
                                        "\n",
                                        f"Addresses redacted: {total_numberof_addressesRedacted}", 
                                        "\n",
                                       
                                    ]
                                ) 
                               stat_file.write(statisitics_results)
                               total_numberof_namesRedacted = 0
                               total_numberof_datesRedacted = 0
                               total_numberof_phoneNumRedacted = 0
                               total_numberof_genderTermsRedacted = 0
                               total_numberof_addressesRedacted= 0
                                
       else:
            print(
                f"There is no file that matches for the given {pattern} glob pattern. Please try another pattern",
                file=stderr,
            )

     

   
   
   
     ###############  MAIN CODE ######################
if __name__ == "__main__":
     parse = argparse.ArgumentParser()
     
     parse.add_argument(
              "--input",
              nargs="+",
              type=str,
              required=True,
              help="this is a pattern via glob to take input file format",
     )
     parse.add_argument(
         "--output",
         type=str,
         required=True,
         help="it will have a directory location to save the redacted version of files",   
     )
     parse.add_argument(
         "--stats",
         type=str,
         required=True,
         help="it will have location to write the stats of files redactred",
    )
    
     redaction_options=["--names","--dates","--address","--phones","--genders"]
     for option in redaction_options:
         parse.add_argument(option,action="store_true",help=f"it is a flag which while entered will redact all {option[2:]} from the file")

    ##parsing the command line arguments 
     argument=parse.parse_args()

    #dictionary of all the arguments which were inputted via terminal
     dictionary_with_all_arguments = vars(argument) 
    
     path_pattern_input_file= ""
     folder_path_for_output_files=""
     statistics_display_place=""
     redaction_flags=[]

     for key in dictionary_with_all_arguments:
         if key=="input":
             path_pattern_input_file=dictionary_with_all_arguments["input"]
         elif key=="output":
             output_path_of_redacted_files=dictionary_with_all_arguments["output"]
         elif key=="stats":
              statistics_display_place=dictionary_with_all_arguments["stats"]
         else:
             redaction_flags.append(key)

    
     main(path_pattern_input_file,redaction_flags,output_path_of_redacted_files, statistics_display_place,)