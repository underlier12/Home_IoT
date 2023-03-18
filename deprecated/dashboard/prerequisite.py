from elasticsearch_module import ElasticsearchModule

def main():
    em = ElasticsearchModule()
    INDEX = ['tempnhumi', 'charges']
    
    for i in INDEX:
        if not em.check_existing_index(i):
            em.make_index(i)

if __name__ == "__main__":
    main()