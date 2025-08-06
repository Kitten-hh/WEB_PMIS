from django.conf import settings
from ..models import AiSentences
from datetime import datetime
from BaseApp.library.tools import AsyncioTools

class AiSentencesService:
    def generate_sentences(self, reference_type=None, data=[], paraphrase_count=3, gpt_model='gpt3', append=True, generate_embedding=False):
        try:
            if reference_type and data:
                paraphrase_url = "{0}/api/paraphrase/".format(settings.AI_RESTAPI_SERVER)

                paraphrase_http_methods = {
                    'url': paraphrase_url,
                    'method': 'POST',
                    'params': {'data': data, 'fields': ['sentence'], 'gpt_model': gpt_model, 'paraphrase_count': paraphrase_count},
                    'basic_auth_user': settings.AI_REST_API_USERNAME,
                    'basic_auth_password': settings.AI_REST_API_PASSWORD
                }
                target_languages = ['English', 'Chinese']  # 生成的语言
                ai_sentences_data = []
                original_sentences_data = [{"reference_id":row['reference_id'], "sentence":row['sentence'], "language":None} for row in data]

                # Iterate over target languages to generate paraphrased sentences
                for lang in target_languages:
                    paraphrase_http_methods['params']['target_language'] = lang
                    paraphrase_response = AsyncioTools.async_fetch_http_json({"data": paraphrase_http_methods})
                    paraphrase_result = paraphrase_response['data']

                    if paraphrase_result['status']:
                        paraphrased_data = paraphrase_result.get("data", [])
                        for paraphrased in paraphrased_data:
                            reference_id = paraphrased.get("reference_id")
                            sentences = paraphrased.get(f"sentence_paraphrases_{lang.lower()}", [])

                            # Save paraphrased sentences
                            for paraphrased_sentence in sentences:
                                ai_sentences_data.append({
                                    "sentence": paraphrased_sentence,
                                    "reference_id": reference_id,
                                    "language": lang
                                })

                # Append or overwrite generated sentences to the database
                if ai_sentences_data or original_sentences_data:
                    if append:
                        self.__save_sentences(original_sentences_data + ai_sentences_data, reference_type)
                    else:
                        self.__delete_and_create_sentences(original_sentences_data + ai_sentences_data, reference_type)

                    if generate_embedding:
                        # Generate embeddings for the newly created or updated sentences
                        reference_ids = [sentence['reference_id'] for sentence in data]
                        sentences_for_embedding = list(AiSentences.objects.filter(reference_id__in=reference_ids, reference_type=reference_type, embedding_vector=None).values('reference_id', 'sentence'))
                        self.generate_embeddings(reference_type, sentences_for_embedding)

        except Exception as e:
            # Logging or error handling can be added here
            print(f"Error generating sentences: {e}")

    def __save_sentences(self, ai_sentences_data, reference_type):
        try:
            # Save paraphrased sentences to AiSentences table
            for sentence in ai_sentences_data:
                if not AiSentences.objects.filter(
                    reference_id=sentence['reference_id'],
                    reference_type=reference_type,
                    sentence=sentence['sentence']
                ).exists():
                    AiSentences.objects.create(
                        reference_id=sentence['reference_id'],
                        reference_type=reference_type,
                        sentence=sentence['sentence'],
                        language=sentence['language'],
                        embedding_vector=None,
                        created_at=datetime.now()
                    )
        except Exception as e:
            # Handle exceptions related to database operations
            print(f"Error saving sentences: {e}")

    def __delete_and_create_sentences(self, ai_sentences_data, reference_type):
        try:
            # Delete existing sentences and create new ones in AiSentences table
            reference_ids = set(sentence['reference_id'] for sentence in ai_sentences_data)
            AiSentences.objects.filter(reference_id__in=reference_ids, reference_type=reference_type).delete()
            for sentence in ai_sentences_data:
                AiSentences.objects.create(
                    reference_id=sentence['reference_id'],
                    reference_type=reference_type,
                    sentence=sentence['sentence'],
                    language=sentence['language'],
                    embedding_vector=None,
                    created_at=datetime.now()
                )
        except Exception as e:
            # Handle exceptions related to database operations
            print(f"Error deleting and creating sentences: {e}")

    def generate_embeddings(self,reference_type, data=[], field='sentence', model='text-embedding-ada-002'):
        try:
            if data:
                embedding_url = "{0}/api/embedding/openai".format(settings.AI_RESTAPI_SERVER)
                embedding_http_methods = {
                    'url': embedding_url,
                    'method': 'POST',
                    'params': {'data': data, 'field': field, 'model': model},
                    'basic_auth_user': settings.AI_REST_API_USERNAME,
                    'basic_auth_password': settings.AI_REST_API_PASSWORD
                }
                print(embedding_http_methods)
                embedding_response = AsyncioTools.async_fetch_http_json({"data": embedding_http_methods})
                embedding_result = embedding_response['data']
            
                if embedding_result['status']:
                    embeddings_data = embedding_result.get("data", [])
                    # Save embeddings to AiSentences table
                    for item in embeddings_data:
                        reference_id = item.get("reference_id")
                        embedding_vector = item.get("sentence_embedding")
                        if reference_id and embedding_vector:
                            AiSentences.objects.filter(reference_type=reference_type, reference_id=reference_id).update(
                                embedding_vector=embedding_vector
                            )
                    return embeddings_data
                else:
                    print(f"Error generating embeddings: {embedding_result.get('msg', 'Unknown error')}")
                    return []
        except Exception as e:
            # Handle exceptions related to embedding generation
            print(f"Error generating embeddings: {e}")
            return []
