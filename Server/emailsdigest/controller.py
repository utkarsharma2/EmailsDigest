import json
import ssl
import uuid

import nltk
import numpy as np
import pandas as pd
from django.core.mail import EmailMessage
from emailsdigest import models
from nltk.corpus import stopwords
from Server import settings

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


def get_emails_bucket(app):
    """Get all bucket representator emails which are not sent"""
    return models.Email.objects.filter(app=app, is_sent=False, is_leader=True)


def cal_TFIDF(emails):
    """Calculate the similarity array"""

    documents_df=pd.DataFrame(emails,columns=['documents'])
    
    # Remove stop words
    stop_words_l=stopwords.words('english')
    documents_df['documents_cleaned']=documents_df.documents.apply(lambda x: " ".join(re.sub(r'[^a-zA-Z]',' ',w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]',' ',w).lower() not in stop_words_l))
    tfidfvectoriser=TfidfVectorizer()
    tfidfvectoriser.fit(documents_df.documents_cleaned)
    tfidf_vectors=tfidfvectoriser.transform(documents_df.documents_cleaned)
    return np.dot(tfidf_vectors,tfidf_vectors.T).toarray()


def format_email(subject, body):
    """get formatted subject and body of email"""
    return subject + " --  " + body


def label_email(email, app):
    """Get label for email"""

    # Get emails that represent buckets
    emails = list(get_emails_bucket(app))

    # Convert them from object to string.
    emails_str = [format_email(x.subject, x.body) for x in emails]
    emails_str.append(format_email(email["subject"], email["body"]))

    # Find pairwise similarity
    pairwise_similarities = cal_TFIDF(emails_str)

    # iterate over similarity for last email.
    index = 0
    labels = []
    for similarities in pairwise_similarities[-1]:		
        if index == len(emails_str) - 1:
            continue

        # check if any bucket email crosses threshold and assign same label
        if (1 - similarities) <= app.threshold:
            labels.append(emails[index].label)

        index += 1
    
    if len(labels) == 1:
        return labels[0], False
    elif len(labels) > 1:
        return merge_labels(labels), False

    # if email is unique assign new label
    return uuid.uuid1(), True

def prepare_labels_for_merge(app):
    emails = list(get_emails_bucket(app))
    emails_str = [format_email(x.subject, x.body) for x in emails]

    pairwise_similarities = cal_TFIDF(emails_str)
    
    email_index_x = 0
    email_index_y = 0
    list_of_sets = []
    for emails_similarities in pairwise_similarities:
        email_index_x = 0
        for similarities in emails_similarities:
            if email_index_x == email_index_y:
                continue
            
            if (1 - similarities) <= app.threshold:
                
                match = False
                for _set in list_of_sets:
                    if  emails[email_index_x].label in _set \
                         or emails[email_index_y].label in _set:

                        _set.update([
                            emails[email_index_y].label,
                            emails[email_index_x].label
                        ])
                        match = True

                if not match:
                    list_of_sets.append(set([
                        emails[email_index_y].label,
                        emails[email_index_x].label
                    ]))
    
            email_index_x += 1
        email_index_y += 1

    return list_of_sets

def merge_leaders_emails(app):
    list_of_labels = prepare_labels_for_merge(app)
    is_merged = False
    for labels in list_of_labels:
        merge_labels(list(labels))
        is_merged = True
    return is_merged

def send_email(subject, body, to):
    """Send email"""
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_EMAIL_FROM,
        to=to
    )
    email.send(fail_silently=False)

def check_params(param_list, query_params):
        """Check required params"""
        for param in param_list:
            if query_params.get(param) is None:
                return False
        return True

def merge_labels(labels):
    if len(labels) == 0:
        raise Exception('Empty label list passed.')
    elif len(labels) == 1:
        return labels[0]
    else:
        leader_label = labels.pop()
        models.Email.objects.filter(label__in=labels, is_sent=False).update(label=leader_label)
    return leader_label