import redactor
from redactor import redact_phnumber ,terms_to_be_redacted ,remove_char,redact_names,redact_address,redact_dates,redact_genderTerms
from base64 import decode
import redactor
from spacy import tokens
import pytest


def sample_test_document():
    test_file = open('./test.txt')
    test_string = test_file.read()
    return test_string

def test_remove_char():
    instance=sample_test_document()
    clean_tokens = remove_char(instance)
    assert isinstance(clean_tokens, list) == True
    assert isinstance(clean_tokens[0], tokens.token.Token) == True


def test_redact_phonenums():
    instance=sample_test_document()
    redact_phnumber(instance)
    assert isinstance(terms_to_be_redacted[0],tuple) == True

def test_redact_names():
    instance=sample_test_document()
    final_instance=remove_char(instance)
    redact_names(final_instance)
    assert isinstance(terms_to_be_redacted[0],tuple) == True

def test_redact_dates():
    instance= sample_test_document()
    final_instance=remove_char(instance)
    redact_dates(final_instance)
    assert isinstance(terms_to_be_redacted[0],tuple) == True

def test_redact_address():
    instance= sample_test_document()
    final_instance=remove_char(instance)
    redact_address(final_instance)
    assert isinstance(terms_to_be_redacted[0],tuple) == True

def test_redact_genders():
    final_instance= sample_test_document()
    final_instance=remove_char(final_instance)
    redact_genderTerms(final_instance)
    assert isinstance(terms_to_be_redacted[0],tuple) == True
    
