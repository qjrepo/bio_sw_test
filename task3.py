import requests
from tabulate import tabulate

def retrieve_information(variant_ids):
    # Ensembl REST API endpoint
    ensembl_url = 'https://rest.ensembl.org/'

    # output table headers
    headers = ['Variant ID', 'Alleles', 'Locations', 'Effects', 'Genes']
    rows = []

    for variant_id in variant_ids:
        try:
            # call /variation/human/{variant_id} endpoint to retrieve data about alleles, locations, and then add them to their respective array
            variant_endpoint = f'{ensembl_url}/variation/human/{variant_id}'
            variant_response = requests.get(variant_endpoint, headers = {'Content-Type': 'application/json'})

            alleles = []
            locations = []

            if variant_response.ok:
                variant_data = variant_response.json()
                
                if 'mappings' in variant_data and variant_data['mappings']:
                    for mapping in variant_data['mappings']:
                        if 'allele_string' in mapping:
                            if mapping['allele_string'] not in alleles:
                                alleles.append(mapping['allele_string'])
                        if 'location' in mapping:
                            location = mapping['location']
                            locations.append(location)
            else:
                print(f'Error when getting the alleles and locations data for {variant_id}')
            
            # call the /vep/human/id/{variant_id} endpoint to retrieve data about effects and add them to the effects array
            # also find all the transcript_ids in order to find the genes that contain the transcripts
            effects = []

            consequence_endpoint = f'{ensembl_url}/vep/human/id/{variant_id}'
            consequence_response = requests.get(consequence_endpoint, headers = {'Content-Type': 'application/json'})
            
            transcript_ids = []
            genes = []

            if consequence_response.ok:
                consequence_data = consequence_response.json()
               
                if 'transcript_consequences' in consequence_data[0] and consequence_data[0]['transcript_consequences']:
                    for consequence in consequence_data[0]['transcript_consequences']:
                        if 'consequence_terms' in consequence:
                            if consequence['consequence_terms']:
                                effects.extend(consequence['consequence_terms'])
                        if 'transcript_id' in consequence:
                            transcript_ids.append(consequence['transcript_id'])

                # to look up all the genes that contain the transcripts in the transcript_id array
                # by calling /lookup/id/{transcript_id} endpoint and add them to the genes array
                for transcript_id in transcript_ids:
                    gene_endpoint = f'{ensembl_url}/lookup/id/{transcript_id}'
                    gene_response = requests.get(gene_endpoint, headers = {'Content-Type': 'application/json'})

                    if gene_response.ok:
                        gene_data = gene_response.json()
                        if 'display_name' in gene_data:
                            genes.append(gene_data['display_name'])
                    else:
                        print(f'Error when getting the gene name for {transcript_id} for {variant_id}')
            else:
                print(f'Error when getting the effects data for {variant_id}')

            # concatenate the elements in each array, seperated by comma and add the row to output rows
            if not alleles:
                alleles_str = 'Not available'
            else:
                alleles_str = ','.join(alleles)

            if not locations:
                locations_str = 'Not available'
            else:
                locations_str = ','.join(locations)

            if not effects:
                effects_str = 'Not available'
            else:
                effects_str = ','.join(effects)

            # if not transcript_ids:
            #     transcript_ids_str = 'Not available'
            # else:
            #     transcript_ids_str = ','.join(transcript_ids)

            if not genes:
                genes_str = 'Not available'
            else:
                genes_str = ','.join(genes)

            rows.append([variant_id, alleles_str, locations_str, effects_str, genes_str])

        except requests.exceptions.RequestException as e:
            print(f'Error when getting the data for {variant_id}. Error msg: {str(e)}')

    # print(tabulate(rows, headers=headers, tablefmt='grid'))

    table = tabulate(rows, headers=headers, tablefmt='grid')
    return table

if __name__ == "__main__":
    variant_ids = ['rs56116432']
    print(retrieve_information(variant_ids))


            
                


                        






            


                            




