# import os
# import traceback
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_community.vectorstores import FAISS

# def generate_data(ingredients_list):
#     try:
#         # Set environment variables for API keys
#         os.environ["GOOGLE_API_KEY"] = "AIzaSyC6-JLG5Q_bkHayQZ8MJBF5Cg8ii6TndEU"
#         os.environ["LANGCHAIN_API_KEY"] = "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"
#         os.environ["LANGCHAIN_TRACING_V2"] = "true"

#         # Initialize embeddings and vector store
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         vector_store = FAISS.load_local("database", embeddings, allow_dangerous_deserialization=True)

#         # Create retriever
#         retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 50})

#         # Define improved prompt template
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", """For the given list of ingredients separated by ';', provide detailed information including:
#             - Banned in USA
#             - Banned in EU
#             - Contains sulfates, parabens, synthetic colors, fragrance, triclosan, toluene, talc, lead, PEG, formaldehyde, diethanolamine, alcohol, hydroquinone
#             - Any other harmful chemicals
#             - Indicate if they are naturally occurring
#             Please return this information in CSV format with the following headers:
#             ingredient,USA,EU,sulfates,parabens,phthalates,synthetic_colors,fragrance,triclosan,toluene,talc,lead,PEG,formaldehyde,diethanolamine,alcohol,hydroquinone,other_info,natural
#             Example output:
#             ingredient,USA,EU,sulfates,parabens,...
#             "water","no","no","no","no","no",..."""),
#             ("human", "{input}"),
#         ])

#         # Initialize the language model
#         llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=None)

#         # Create a chain to parse the output
#         output_parser = StrOutputParser()
#         question_answer_chain = create_stuff_documents_chain(llm, prompt)
#         rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#         # Invoke the chain with the input list of ingredients
#         response = rag_chain.invoke({"input": ingredients_list})

#         # Debug print for the full response
#         print("Full response received:\n", response)

#         # Process the answer
#         answer = response.get('answer', '').strip()
#         if not answer:
#             print("No valid answer received from the model.")
#             return

#         # Debug print for the response
#         print("Generated response:\n", answer)

#         # Write the response to a CSV file
#         output_path = os.path.join("output.csv")
#         with open(output_path, 'w', encoding='utf-8') as f:
#             f.write(answer)
        
#         print(f"Output successfully written to {output_path}")

#     except Exception as e:
#         print("An error occurred:")
#         traceback.print_exc()

# Example usage of the function
# ingredients_list = "(1 methyl 2 (5 methylhex 4 en 2 yl)cyclopropyl)methanol; (5,6)fullerene c60; (trifolium pratense (clover)/vigna radiata) sprout extract"
# generate_data(ingredients_list)

# Example usage
# ingredients_list = "ingredient1;ingredient2;ingredient3"
# generate_data(ingredients_list)















# import sys
# import os
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_community.vectorstores import FAISS

# def generate_data(ingredients_list):

#     os.environ["GOOGLE_API_KEY"] = "AIzaSyAFRtlvbZCNiZJYZryYslw9lEqEsYgdgs0"
#     os.environ["LANGCHAIN_API_KEY"] = "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"
#     os.environ["LANGCHAIN_TRACING_V2"] = "true"

#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     vector_store = FAISS.load_local(
#         "database", embeddings, allow_dangerous_deserialization=True
#     )

#     retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 50})

#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 """For the given list of ingredients separated by ';', state yes or no, with some additional information if necessary, for the following details: 
#                 Banned in USA, banned in EU, contains sulphates, contains parabens, contains synthetic colors, contains fragrance, contains triclosan, 
#                 contains toluene, contains talc, contains lead, contains polyethylene Glycol (PEG), contains formaldehyde, contains diethanolamine, 
#                 contains alcohol, contains hydroquinone, state if they are naturally occurring and if contains any other harmful chemicals. 
#                 Make sure to return a string in CSV format along with the header only.
#                 For example:
#                 ingredient,USA,EU,sulfates,parabens,phthalates,synthetic_colors,fragrance,triclosan,toluene,talc,lead,PEG,formaldehyde,diethanolamine,alcohol,hydroquinone,other_info,natural
#                 "water","no","no","no","no","no","no","no","no","no","no","no","no","no","no","no","no","None","yes"
#                 "glycerine","no","no","no","no","no","no","no","no","no","no","no","no","no","no","no","Can be derived from natural sources","yes"
#                 Use this information about the ingredients as additional context for generating results"""
#                 "\n\n"
#                 "{context}"
#             ),
#             ("human", "{input}"),
#         ]
#     )

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-pro",
#         temperature=0,
#         max_tokens=None,
#     )

#     output_parser = StrOutputParser()
#     question_answer_chain = create_stuff_documents_chain(llm, prompt)
#     rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#     response = rag_chain.invoke({"input": ingredients_list})
#     answer = response['answer'].strip()
#     output_path = os.path.join("output.csv")
#     with open(output_path, 'w') as f:
#         f.write(answer)



# import sys
# import os
# import traceback
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_community.vectorstores import FAISS

# def generate_data(ingredients_list):
#     try:
#         # Set environment variables for API keys
#         os.environ["GOOGLE_API_KEY"] = "AIzaSyC6-JLG5Q_bkHayQZ8MJBF5Cg8ii6TndEU"
#         os.environ["LANGCHAIN_API_KEY"] = "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"
#         os.environ["LANGCHAIN_TRACING_V2"] = "true"

#         # Initialize embeddings and vector store
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         vector_store = FAISS.load_local(
#             "database", embeddings, allow_dangerous_deserialization=True
#         )

#         # Create retriever
#         retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 50})

#         # Define prompt template
#         prompt = ChatPromptTemplate.from_messages(
#             [
#                 (
#                     "system",
#                     """For the given list of ingredients separated by ';', state yes or no, with some additional information if necessary, for the following details: 
#                     Banned in USA, banned in EU, contains sulphates, contains parabens, contains synthetic colors, contains fragrance, contains triclosan, 
#                     contains toluene, contains talc, contains lead, contains polyethylene Glycol (PEG), contains formaldehyde, contains diethanolamine, 
#                     contains alcohol, contains hydroquinone, state if they are naturally occurring and if contains any other harmful chemicals. 
#                     Make sure to return a string in CSV format along with the header only.
#                     For example:
#                     ingredient,USA,EU,sulfates,parabens,phthalates,synthetic_colors,fragrance,triclosan,toluene,talc,lead,PEG,formaldehyde,diethanolamine,alcohol,hydroquinone,other_info,natural
#                     "water","no","no","no","no","no","no","no","no","no","no","no","no","no","no","no","no","None","yes"
#                     "glycerine","no","no","no","no","no","no","no","no","no","no","no","no","no","no","no","Can be derived from natural sources","yes"
#                     Use this information about the ingredients as additional context for generating results"""
#                     "\n\n"
#                     "{context}"
#                 ),
#                 ("human", "{input}"),
#             ]
#         )

#         # Initialize the language model
#         llm = ChatGoogleGenerativeAI(
#             model="gemini-1.5-pro",
#             temperature=0,
#             max_tokens=None,
#         )

#         # Create a chain to parse the output
#         output_parser = StrOutputParser()
#         question_answer_chain = create_stuff_documents_chain(llm, prompt)
#         rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#         # Invoke the chain with the input list of ingredients
#         response = rag_chain.invoke({"input": ingredients_list})

#         # Check and handle the response
#         if 'answer' not in response or not response['answer']:
#             print("No valid answer received from the model.")
#             return

#         # Process the answer
#         answer = response['answer'].strip()

#         # Debug print for the response
#         print("Generated response:\n", answer)

#         # Write the response to a CSV file
#         output_path = os.path.join("output.csv")
#         with open(output_path, 'w') as f:
#             f.write(answer)
        
#         print(f"Output successfully written to {output_path}")

#     except Exception as e:
#         print("An error occurred:")
#         traceback.print_exc()

# Example usage of the function
# ingredients_list = "(1 methyl 2 (5 methylhex 4 en 2 yl)cyclopropyl)methanol; (5,6)fullerene c60; (trifolium pratense (clover)/vigna radiata) sprout extract"
# generate_data(ingredients_list)
import os
import traceback
import csv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS

def clean_quotes(text):
    # Remove excessive triple quotes and unnecessary whitespace
    return text.replace('"""', '"').strip()

def generate_data(ingredients_list):
    try:
        # Set environment variables for API keys
        os.environ["GOOGLE_API_KEY"] = "AIzaSyAl_4HgUabMTBoWTUyezihM5qJBjV-3uDI"
        os.environ["LANGCHAIN_API_KEY"] = "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"
        os.environ["LANGCHAIN_TRACING_V2"] = "true"

        print(os.getenv("LANGCHAIN_API_KEY"))
        # Initialize embeddings and vector store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.load_local("database", embeddings, allow_dangerous_deserialization=True)

        # Create retriever
        retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 50})

        # Define the prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """For the given list of ingredients separated by ';', state yes or no, with some additional information if necessary, for the following details: 
                    Banned in USA, banned in EU, contains sulphates, contains parabens, contains synthetic colors, contains fragrance, contains triclosan, 
                    contains toluene, contains talc, contains lead, contains polyethylene Glycol (PEG), contains formaldehyde, contains diethanolamine, 
                    contains alcohol, contains hydroquinone, state if they are naturally occurring and if they contain any other harmful chemicals. 
                    Make sure to return a string in CSV format along with the header only.
                    For example:
                    ingredient,USA,EU,sulfates,parabens,phthalates,synthetic_colors,fragrance,triclosan,toluene,talc,lead,PEG,formaldehyde,diethanolamine,alcohol,hydroquinone,other_info,natural
                    "water","no","no","no","no","no","no","no","no","no","no","no","no","no","no","no","None","yes"
                    "glycerine","no","no","no","no","no","no","no","no","no","no","no","no","no","no","no","Can be derived from natural sources","yes"
                    Use this information about the ingredients as additional context for generating results."""
                ),
                ("human", "{input}\n\n{context}"),
            ]
        )

        # Initialize the language model
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=None)

        # Create a chain to parse the output
        output_parser = StrOutputParser()
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        # Invoke the chain with the input list of ingredients
        response = rag_chain.invoke({"input": ingredients_list})

        # Process the answer
        answer = response.get('answer', '').strip()
        if not answer:
            print("No valid answer received from the model.")
            return ""

        # Clean up the triple quotes before writing to CSV
        cleaned_answer = clean_quotes(answer)

        # Append the cleaned answer to the CSV file
        csv_filename = "ingredientoutput.csv"
        # Write or append the data to the CSV file
        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header only if the file does not already exist
            if not file_exists:
                csv_writer.writerow([
                    "ingredient", "USA", "EU", "sulfates", "parabens", "phthalates",
                    "synthetic_colors", "fragrance", "triclosan", "toluene", "talc",
                    "lead", "PEG", "formaldehyde", "diethanolamine", "alcohol",
                    "hydroquinone", "other_info", "natural"
                ])
            
            # Split the cleaned answer by lines and write each line to the CSV
            for line in cleaned_answer.splitlines():
                if line.strip():  # Avoid empty lines
                    csv_writer.writerow([value.strip().strip('"') for value in line.split(',')])

        print(f"Output successfully appended to {csv_filename}")
        return cleaned_answer  # Return the generated answer

    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
        return ""

# Example usage
if __name__ == "__main__":
    ingredients_list = "sodium stannate; sodium starch octenylsuccinate; sodium stearate; sodium stearate; sodium stearate; sodium stearoamphoacetate; sodium stearoyl glutamate; sodium stearoyl lactylate; sodium stearoyl lactylate; sodium styrene/ acrylates copolymer; sodium styrene/acrylates/peg 10 dimaleate copolymer; sodium succinate; sodium sulfate; sodium sulfite; sodium sulfoacetate; sodium sunflower seedate; sodium sunflowerseedamphoacetate; sodium sunflowerseedamphoacetate; sodium surfactin; sodium surfactin; sodium sweetalmondamphoacetate; sodium tallowate; sodium taurine cocoyl methyltaurate; sodium taurine cocoyl methyltaurate; sodium taurine laurate; sodium thioglycolate; sodium thiosulfate; sodium thiosulfate; sodium trideceth sulfate; sodium trideceth sulfate; sodium tripolyphosphate; sodium usnate; sodium xylene sulfonate; sodium xylene sulfonate; sodium zinc polyitaconate; solanum lycopersicum (tomato); solanum lycopersicum (tomato) callus culture extract; solanum lycopersicum (tomato) extract; solanum lycopersicum (tomato) seed oil; solanum melongena (eggplant) fruit extract; solanum paniculatum extract; solanum tuberosum (potato) extract; solanum tuberosum (potato) starch; solidago virgaurea (goldenrod) extract; soluble collagen; soluble collagen; solum diatomeae; solum fullonum; solvent red 48 or acid red 92 (uncertified d&c red no. 27 or d&c red no. 28); solvent red 48 or acid red 92 (uncertified d&c red no. 27 or d&c red no. 28); sophora angustifolia root extract; sophora japonica (japanese pagoda tree) extract; sorbeth 230 tetraoleate; sorbeth 30 tetraisostearate; sorbeth 30 tetraisostearate; sorbeth 30 tetraoleate; sorbic acid; sorbitan; sorbitan caprylate; sorbitan ester; sorbitan ester; sorbitan ester; sorbitan ester; sorbitan ester; sorbitan isostearate; sorbitan laurate; sorbitan oleate; sorbitan oleate decylglucoside crosspolymer; sorbitan olivate; sorbitan palmitate; sorbitan sesquiisostearate; sorbitan sesquioleate; sorbitan sesquistearate; sorbitan stearate; sorbitan trioleate; sorbitan trioleate; sorbitan tristearate; sorbitol; sorbitol; sorbitol laurate; sorbitol/sebacic acid copolymer behenate; sorbus aucuparia fruit ferment filtrate; soy acid; soy acid; soy amino acids; soy isoflavones; soy protein phthalate; soyaethyl morpholinium ethosulfate; soyamide dea; soyamidopropalkonium chloride; soyamidopropylamine oxide; soyamine; soybean glycerides; soymilk; soytrimonium chloride; soytrimonium chloride; sparassis crispa extract; sparteine, ( ); spartium junceum flower extract; sphinganine; spilanthes acmella flower extract; spinacia oleracea (spinach) leaf extract; spiraea ulmaria (meadowsweet) extract; spiraea ulmaria (meadowsweet) flower extract; spiraea ulmaria (meadowsweet) leaf extract; spiro(16,18 methano 1 h,3 h,23 h (1,6,12)trioxacyclooctadecino(3,4 d)(1)benzopyran 17(18 h),2'; spiro(16,18 methano 1 h,3 h,23 h (1,6,12)trioxacyclooctadecino(3,4 d)(1)benzopyran 17(18 h),2'; spirulina; spirulina; spirulina maxima (algae); spirulina maxima (algae) extract; spirulina platensis extract; spirulina platensis powder; spruce oil; squalane; squalane oil; squalene oil; sr hydrozoan polypeptide 1; stannous chloride; stannous fluoride; starch; starch acetate; starch hydroxypropyl ester; starch hydroxypropyltrimonium chloride; starch octenylsuccinate; steapyrium chloride; steapyrium chloride; stearalkonium bentonite; stearalkonium chloride; stearalkonium hectorite; stearamide amp; stearamide mea; stearamidoethyl diethylamine; stearamidoethyl diethylamine; stearamidopropyl; stearamidopropyl dimethylamine; stearamidopropyl dimethylamine lactate; stearamidopropyl pg dimonium chloride; stearamidopropyl pg dimonium chloride phosphate; stearamine oxide; stearate; steardimonium hydroxypropyl hydrolyzed keratin; steardimonium hydroxypropyl hydrolyzed wheat protein; steareth 10; steareth 10 allyl ether/acrylates copolymer; steareth 100; steareth 100; steareth 100/peg 136/hdi copolymer; steareth 2; steareth 20; steareth 21; steareth 25; steareth 4; steareth 40; steareth 6; steareth 80; stearic acid; stearoxydimethicone; stearoxymethicone/ dimethicone copolymer; stearoxypropyl dimethylamine; stearoxytrimethylsilane; stearoyl; stearoyl glutamate; stearoyl glutamic acid; stearoyl inulin; stearoyl stearate; steartrimonium chloride; steartrimonium chloride; stearyl alcohol; stearyl beeswax; stearyl behenate; stearyl benzoate; stearyl caprylate; stearyl citrate; stearyl dihydroxypropyldimonium oligosaccharides; stearyl dimethicone; stearyl esters; stearyl glycol; stearyl glycyrrhetinate; stearyl heptanoate; stearyl methicone; stearyl octyldimonium methosulfate; stearyl octyldimonium methosulfate; stearyl octyldimonium methosulfate; stearyl palmitate; stearyl phosphate; stearyl ppg 3 myristyl ether dimer dilinoleate; stearyl stearate; stearyl stearoyl stearate; stearyl triethoxysilane; stearyldimoniumhydroxypropyl decylglucosides chloride; stearyldimoniumhydroxypropyl laurylglucosides chloride; stellaria media (chickweed); stellaria media (chickweed) extract; sterol; stevia glycerite; stevia rebaudiana (sweetleaf) extract; stevioside; stevioside; stevioside; strontium peroxide; styrax tonkinensis resin extract; styrene; styrene/ butadiene copolymer; styrene/ pvp copolymer; styrene/acrylamide copolymer; styrene/acrylates copolymer; styrene/acrylates/ammonium methacrylate copolymer; styrene/isoprene copolymer; subtilisin; succinic acid; succinoglycan; succinoglycan; sucralose; sucrose; sucrose acetate; sucrose acetate isobutyrate; sucrose benzoate; sucrose cocoate; sucrose dilaurate; sucrose dilaurate; sucrose distearate; sucrose laurate; sucrose myristate; sucrose palmitate; sucrose polycottonseedate; sucrose polystearate; sucrose stearate; sucrose tetraisostearate; sucrose tetrastearate triacetate; sucrose trilaurate; sulfated castor oil; sulfonic acid; sulfur; sulfuric acid; sulfuric acid alkyl esters (c12 18), sodium salts; sulisobenzone; sulisobenzone; sulphur dioxide; sunflower oil decyl esters; sunflower oil/palm oil aminopropanediol esters; sunflower seed oil glycereth 8 esters; sunflower seed oil glycereth 8 esters; sunflower seed oil glyceride; sunflower seedamidopropyl dimethylamine lactate; sunflowerseedamidopropyl ethyldimonium ethosulfate; superoxide dismutase; sweet pea oil; swertia chirata extract; swertia japonica (semburi) extract; symphytum officinale (comfrey); symphytum officinale (comfrey) extract; symphytum officinale (comfrey) leaf; symphytum officinale (comfrey) leaf extract; symphytum officinale (comfrey) root; symphytum officinale (comfrey) root extract; symphytum officinale leaf powder; synthetic beeswax; synthetic beeswax; synthetic candelilla wax; synthetic carnauba; synthetic fluorphlogopite; synthetic japan wax; synthetic japan wax; synthetic jojoba oil; synthetic sapphire; synthetic wax; synthetic wax; syringa vulgaris (lilac) extract; syringa vulgaris (lilac) flower extract; syringa vulgaris leaf cell culture extract; syzygium aromatica (clove bud) oil; syzygium aromaticum (clove); syzygium aromaticum (clove) flower oil; syzygium aromaticum (clove) flower oil; syzygium aromaticum (clove) flower oil; syzygium caryophyllata (clove bud) oil; syzygium caryophyllata (clove bud) oil; syzygium caryophyllata (clove bud) powder; syzygium caryophyllata (clove bud) powder; syzygium leuhmanii fruit extract; syzygium luehmannii (lilly pilly) fruit extract; t butyl alcohol; tabebuia impetiginosa (pau d'arco); tagetes erecta; tagetes minuta (muster john henry) oil; tagetes minuta flower oil; talc; tall oil; tall oil acid; tall oil glycerides; tallow; tallow fatty acid; tallowtrimonium chloride; tamarindus indica (tamarind) seed polysaccharide; tamarindus indica extract; tamarindus indica fruit extract; tamarindus indica seed gum; tamarindus indica seed gum; tanacetum annuum (blue tansy); tanacetum annuum (blue tansy) flower oil; tanacetum annuum (blue tansy) oil; tanacetum vulgare (tansy) extract; tansy oil; tapioca; tapioca flour; tapioca starch; taraxacum officinale (dandelion); taraxacum officinale (dandelion) extract; taraxacum officinale (dandelion) leaf extract; taraxacum officinale (dandelion) root; taraxacum officinale (dandelion) root extract; taro; tartaric acid; tasiloxane; tasiloxane; tasmannia lanceolata fruit extract; taurine; tdi/trimellitic anhydride copolymer; tea carbomer; tea carbomer; tea cocoyl glutamate; tea dodecylbenzenesulfonate; tea dodecylbenzenesulfonate; tea lauroyl collagen amino acids; tea myristate; tea palmitate; tea salicylate; tea stearate; tea sulfate; tectona grandis (teak) wood extract; tephrosia purpurea seed extract; tephrosia purpurea seed extract; tephrosia purpurea seed extract; terephthalate; terminalia ferdinandiana (kakadu plum) extract; terminalia myriocarpa (indian almond) extract; terpinen 4 ol; terpineol; terpineol acetate; terpineol, alpha; terpinolene; tert butylhydroquinone; tetraaminopyrimidine sulfate; tetrabutyl phenyl hydroxybenzoate; tetradecane; tetradecane; tetradecene; tetradecyl aminobutyroylvalylaminobutyric urea trifluoroacetate; tetradibutyl pentaerithrityl hydroxyhydrocinnamate; tetradibutyl pentaerithrityl hydroxyhydrocinnamate; tetraethylhexanoate; tetrafluoropropene; tetrahexyldecyl ascorbate; tetrahydro 6 pent 2 enyl pyran 2 one; tetrahydro 6 pent 3 enyl pyran 2 one; tetrahydro 6 pent 3 enyl pyran 2 one; tetrahydro dimethylbenzofuran; tetrahydro dimethylbenzofuran; tetrahydro methyl phenyl pyran; tetrahydrobisdemethoxydiferuloylmethane; tetrahydrodemethoxydiferuloylmethane; tetrahydrodiferuloylmethane; tetrahydrofuran; tetrahydrofuran; tetrahydroxypropyl ethylenediamine; tetramethyl acetyloctahydronaphthalenes; tetramethylpyrazine; tetrapeptide 14; tetrapeptide 21; tetrapeptide 28 argininamide; tetrapeptide 29 argininamide; tetrapotassium pyrophosphate; tetraselmis suecica extract; tetrasodium disuccinoyl cystine; tetrasodium edta; tetrasodium etidronate; tetrasodium glutamate diacetate; tetrasodium iminodisuccinate; tetrasodium pyrophosphate; theobroma cacao (cacao) extract; theobroma cacao (cacao) seed oil; theobroma cacao (cocoa) paste; theobroma cacao (cocoa) paste; theobroma cacao (cocoa) seed butter; theobroma cacao (cocoa) shell powder; theobroma cacao fruit powder; theobroma cacao seed powder; theobroma grandiflorum (theobroma); theobroma grandiflorum (theobroma) seed butter; theobromine; theobromine; theobromo cacao (cocoa) powder; theobromo cacao (cocoa) powder; thermus thermophillus ferment; thiamin; thiamine hydrochloride; thiamine hydrochloride; thiamine hydrochloride; thiamine hydrochloride; thiamine nitrate; thioctic acid; thioglycerin; thioglycerin; thioglycolic acid; threonine; thuja occidentalis (arborvitae) leaf oil; thuja occidentalis (arborvitae) leaf oil; thuja occidentalis (arborvitae) leaf oil; thuja occidentalis bark extract; thuja occidentalis leaf extract; thuja orientalis extract; thuja plicata leaf oil; thyme; thymol; thymus mastichina (marjoram) oil; thymus praecox (mother of thyme) extract; thymus serpillum (wild thyme) extract; thymus vulgaris (common thyme); thymus vulgaris (common thyme) leaf extract; thymus vulgaris (common thyme) oil; thymus vulgaris (thyme) extract; thymus vulgaris (thyme) leaf; thymus vulgaris (thyme) leaf; thymus vulgaris (thyme) leaf; thymus zygis oil; tilia cordata (linden) extract; tilia cordata (linden) flower; tilia cordata (linden) flower extract; tilia cordata (linden) oil; tilia europaea flower extract; tilia platyphyllos extract; tilia tomentosa bud extract; tilia tomentosa extract; tin; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tin oxide; tinosorb m; titanium dioxide; titanium dioxide (sunscreen grade); titanium oxide (tio); titanium powder; titanium/titanium dioxide; tocopherol; tocopherol, d alpha; tocophersolan; tocopheryl acetate; tocopheryl glucoside; tocopheryl glucoside; tocopheryl linoleate; tocopheryl linoleate/ oleate; tocopheryl nicotinate; tocotrienols; tolnaftate; toluene; toluene 2,5 diamine; toluenediamine sulfate, p; tonka bean extract; tonka bean oil; topaz; torreya nucifera seed oil; tosylamide; tosylamide/ epoxy resin; tosylamide/ formaldehyde resin; totarol; totarol; tourmaline; trametes versicolor extract; tranexamic acid; trans beta ionone; trans non 2 enal; trans rose ketone 3; trehalose; tremella fuciformis (mushroom) extract; tremella fuciformis sporocarp extract; tri c12 13 alkyl citrate; tri c14 15 alkyl citrate; tri c14 15 alkyl citrate; tri(polyglyceryl 3/lauryl) hydrogenated trilinoleate; triacetin; triacetin; tribehenin; tribehenin peg 20 esters; tribenzoin; tributyl citrate; tributyl citrate; tricalcium phosphate; tricaprin; tricaprylin; tricaprylyl citrate; tricedeth 12; triceteareth 4 phosphate; tricetylmonium chloride; trichilia emetica seed butter; tricholoma matsutake extract; triclocarban; triclosan; tricontanyl pvp; tricontanyl pvp; tricontanyl pvp; tridecane; trideceth 10; trideceth 12; trideceth 15; trideceth 2; trideceth 2 carboxamide mea; trideceth 3; trideceth 5; trideceth 6; trideceth 6 phosphate; trideceth 7; trideceth 7 carboxylic acid; trideceth 8; trideceth 9; trideceth 9 pg amodimethicone; tridecyl alcohol; tridecyl neopentanoate; tridecyl salicylate; tridecyl stearate; tridecyl trimellitate; triethanolamine; triethanolamine lauryl sulfate; triethoxycaprylylsilane; triethoxycaprylylsilane; triethoxysilylethyl polydimethylsiloxyethyl dimethicone; triethoxysilylethyl polydimethylsiloxyethyl hexyl dimethicone; triethyl citrate; triethylene glycol; triethylhexanoin; triethylhexyl trimellitate; trifluoropropyldimethyl/trimethylsiloxysilicate; trifluoropropyldimethyl/trimethylsiloxysilicate; trifolium pratense (clover) leaf extract; trifolium pratense (red clover); trifolium pratense (red clover) extract; trifolium pratense (red clover) extract; trifolium pratense (red clover) extract; trifolium pratense (red clover) flower; triglyceride; triglyceride; trigonella foenum graecum (fenugreek); trigonella foenum graecum fruit extract; trigonella foenum graecum hydroxypropyltrimonium chloride; trigonella foenum graecum seed extract; triheptanoin; trihydroxystearin; trihydroxystearin; triisocetyl citrate; triisodecyl trimellitate; triisononanoin; triisopropanolamine; triisostearate; triisostearin; triisostearoyl polyglyceryl 3 dimer dilinoleate; triisostearyl citrate; trilaureth 4 phosphate; trilaurin; trilinolein; trilinolein; trimellitate; trimellitic anhydride; trimellitic anhydride copolymer; trimethicone; trimethnolamine; trimethoxycaprylylsilane; trimethyl 2 cyclohexenyl 3 pentanone/2 propynol; trimethyl 3 cyclohexene 1 methanethiol; trimethyl hydroxypentyl isobutyrate; trimethyl pentanyl diisobutyrate; trimethyl pentaphenyl trisiloxane; trimethyl pentylcyclopentanone; trimethyl propylcyclohexanepropanol; trimethylbenzoyl diphenylphosphine oxide; trimethylolpropane triacrylate; trimethylolpropane tricaprylate/ tricaprate; trimethylolpropane triethylhexanoate; trimethylolpropane triisostearate; trimethylolpropane trimethacrylate; trimethylpentanediol/adipic acid/glycerin crosspolymer; trimethylpentanediyl dibenzoate; trimethylsiloxane; trimethylsiloxyamodimethicone; trimethylsiloxyphenyl dimethicone; trimethylsiloxysilicate; trimethylsiloxysilicate; trimethylsiloxysilicate/dimethicone crosspolymer; trimethylsiloxysilicate/dimethiconol crosspolymer; trimethylsilylamodimethicone; trimethylundecenal; trimyristin; trioctanion; trioctyldodecyl citrate; triolein; tripalmitin; tripeptide 1; tripeptide 10 citrulline; tripeptide 29; tripeptide 3; triphenyl phosphate; triphenyl trimethicone; tripotassium edta; tripropylene glycol; tris bht mesitylene; tris bht mesitylene; tris(tetramethylhydroxypiperidinol) citrate; trisiloxane; trisodium edta; trisodium glycyrrhizate; trisodium hedta; trisodium inositol triphosphate; trisodium nta; trisodium phosphate; trisodium sulfosuccinate; tristearin; triticum aestivum peptide; triticum vulgare (wheat); triticum vulgare (wheat) bran; triticum vulgare (wheat) bran extract; triticum vulgare (wheat) flour extract; triticum vulgare (wheat) flour lipids; triticum vulgare (wheat) germ; triticum vulgare (wheat) germ acid; triticum vulgare (wheat) germ acid; triticum vulgare (wheat) germ extract; triticum vulgare (wheat) germ glycerides; triticum vulgare (wheat) germ oil; triticum vulgare (wheat) germ oil unsaponifiables; triticum vulgare (wheat) germ oil unsaponifiables; triticum vulgare (wheat) germ powder; triticum vulgare (wheat) gluten; triticum vulgare (wheat) protein; triticum vulgare (wheat) seed extract; triticum vulgare (wheat) starch; tromethamine; tropaeolum majus (nasturtium) extract; tropolone; troxerutin; troxerutin; tryptophan; tuber magnatum extract; tuber melanosporum extract; tulsi (holy basil); turnera diffusa extract; turnera diffusa extract; tussilago farfara (coltsfoot); tussilago farfara (coltsfoot) flower extract; tussilago farfara (coltsfoot) flower extract; tussilago farfara (coltsfoot) flower extract; tussilago farfara (coltsfoot) flower extract; tussilago farfara (coltsfoot) leaf; tussilago farfara (coltsfoot) leaf extract; tyrosine; ubiquinol; ubiquinone; ubiquinone; ulmus davidiana root extract; ulmus fulva (slippery elm); ulmus fulva (slippery elm) bark; ulmus fulva (slippery elm) bark extract; ulmus rubra (slippery elm); ultramarines; ulva lactuca (sea lettuce) extract; undaria pinnatifida extract; undecane; undecenal; undeceth 11; undeceth 3; undeceth 5; undecyl alcohol; undecyl dimethyl oxazoline; undecylenal; undecylenamidopropyl betaine; undecylenic acid; undecylenoyl glycine; undecylenoyl phenylalanine; unspecified color; unspecified color; unspecified extracts; unspecified flavor; unspecified herbs; unspecified inci; unspecified minerals; unspecified preservatives; unspecified waxes; urea; ursolic acid; urtica dioica (nettle); urtica dioica (nettle) extract; urtica dioica (nettle) extract; urtica dioica (nettle) infusion; urtica dioica (nettle) leaf; urtica dioica (nettle) leaf extract; urtica dioica (nettle) leaf powder; urtica dioica (nettle) oil; urtica dioica (nettle) root extract; urtica urens leaf extract; usnea barbata (beard moss); usnea barbata (beard moss) extract; va crotonates/ vinyl neodecanoate copolymer; va crotonates/ vinyl neodecanoate copolymer; va/ crotonates copolymer; va/ vinyl butyl benzoate/ crotonates copolymer; va/butyl maleate/isobornyl acrylate copolymer; vaccinium angustifolium (blueberry) extract; vaccinium angustifolium (blueberry) fruit; vaccinium angustifolium (blueberry) fruit extract; vaccinium angustifolium leaf extract; vaccinium corymbosum (blueberry) fruit; vaccinium corymbosum (blueberry) seed oil; vaccinium macrocarpon (american cranberry) oil; vaccinium macrocarpon (cranberry) fruit; vaccinium macrocarpon (cranberry) fruit extract; vaccinium macrocarpon (cranberry) fruit extract; vaccinium macrocarpon (cranberry) fruit juice; vaccinium macrocarpon (cranberry) seed; vaccinium macrocarpon (cranberry) seed oil; vaccinium macrocarpon seed powder; vaccinium myrtillus (bilberry); vaccinium myrtillus (bilberry) extract; vaccinium myrtillus (bilberry) fruit extract; vaccinium myrtillus (bilberry) fruit extract; vaccinium myrtillus (bilberry) seed oil; vaccinium myrtillus (bilberry) seed oil; vaccinium uliginosum (northern bilberry) extract; vaccinium vitis idaea seed oil; valeriana officinalis (valerian) root; valeriana officinalis collina root extraxt; valeriana wallichii root extract; valeronitrile, 4 (dimethylamino) 2 isopropyl 2 phenyl; valine; valine; vanccinium corybosum (blueberry) extract; vanilla oleoresin; vanilla oleoresin; vanilla planifolia (vanilla); vanilla planifolia (vanilla) bean; vanilla planifolia (vanilla) fruit; vanilla planifolia (vanilla) fruit extract; vanilla planifolia (vanilla) oil; vanilla planifolia seed powder; vanilla resinoid natural; vanilla resinoid natural; vanilla resinoid natural; vanilla tahitensis (vanilla); vanilla tahitensis fruit extract; vanillin; vanillyl butyl ether; vegetable amino acids; vegetable cellulose; vegetable cetearyl glucoside; vegetable cetyl alcohol; vegetable decyl glucoside; vegetable fatty acid; vegetable glyceryl stearate; vegetable gum/ glycerin extract; vegetable oil; vegetable protein; vegetarian glycerin; verbascum thapsus (common mullein) extract; verbascum thapsus (common mullein) extract; verbena (lippia citriodora) oil; verbena (lippia citriodora) oil; verbena officinalis (vervain) extract; verdyl acetate; vernaldehyde; vernaldehyde; vernaldehyde; veronica officinalis (speedwell) extract; veronica officinalis (speedwell) extract; vetiver; vetiver; vetiveria zizanioides (vetiver); vetiveria zizanioides root extract; vetiveria zizanioides root oil; vetiveryl acetate; vibrio alginolyticus ferment filtrate; vigna aconitifolia seed extract; vigna radiata seed extract; vinegar; vinyl caprolactam/ pvp/ dimethylaminoethyl methacrylate copolymer; vinyl dimethicone; vinyl dimethicone/ methicone silsesquioxane crosspolymer; vinyl dimethicone/lauryl dimethicone crosspolymer; vinyl dimethyl/trimethylsiloxysilicate stearyl dimethicone crosspolymer; viola odorata (violet) leaf; viola odorata extract; viola odorata leaf extract; viola odorata oil; viola tricolor (heartsease) flower extract; viola tricolor extract; viola yedoensis extract; virola sebifera nut oil; viscum album (mistletoe) extract; viscum album (mistletoe) leaf extract; visnaga vera fruit/stem extract; vitamin b; vitamin b complex; vitamin b1; vitamin b2; vitamin b3; vitamin b8; vitamin c ester; vitamin c ester; vitamin c ester; vitamin d; vitamin d3; vitamin e succinate; vitamin f; vitamin f; vitamin k; vitamin k2; vitellaria nilotica (east african shea butter); vitex agnus castus extract; vitex trifolia (chaste tree) fruit extract; vitex trifolia (chaste tree) fruit extract; vitis rotundifolia (muscadine grape) fruit extract; vitis rotundifolia (muscadine) seed oil; vitis vinifera (grape); vitis vinifera (grape) flower cell extract; vitis vinifera (grape) fruit extract; vitis vinifera (grape) fruit water; vitis vinifera (grape) juice; vitis vinifera (grape) juice extract; vitis vinifera (grape) juice extract; vitis vinifera (grape) leaf extract; vitis vinifera (grape) leaf oil; vitis vinifera (grape) seed; vitis vinifera (grape) seed extract; vitis vinifera (grape) seed oil; vitis vinifera (grape) skin extract; vitis vinifera (grape) vine extract; voandzeia subterranea seed extract; volcanic ash; volcanic rock; volcanic sand; vp/ acrylates/ lauryl methacrylate copolymer; vp/ dimethylaminoethylmethacrylate copolymer; vp/ dmapa acrylates copolymer; vp/ eicosene copolymer; vp/ hexadecene copolymer; vp/ methacrylamide/ vinyl imidazole copolymer; vp/va copolymer; vp/vinyl caprolactam/dmapa acrylates copolymer; waltheria indica leaf extract; wasabia japonica (japanese horseradish) extract; wasabia japonica (japanese horseradish) root extract; wasabia japonica leaf extract; water; wheat amino acid; wheat amino acids; wheat germ glycerides; wheat germ oil peg 8 esters; wheat germ protein; wheat germamidopropylamine oxide; wheat germamidopropylamine oxide; wheat germamidopropyldimonium hydroxypropyl hydrolyzed wheat protein; wheat germamidopropyldimonium hydroxypropyl hydrolyzed wheat protein; wheat germamidopropyldimonium hydroxypropyl hydrolyzed wheat protein; wheatgermamidopropyl dimethylamine hydrolyzed wheat protein; wheatgermamidopropyl ethyldimonium ethosulfate; wheatgrass; whey protein; whey protein; white clay powder; white petrolatum; white tea; white tea extract; white tea leaf; white tea leaf extract; whole dry milk; wild flower honey; wine; wine extract; wisteria sinensis extract; wisteria sinensis extract; withania somnifera flower extract; withania somnifera flower extract; withania somnifera root extract; withania somnifera root powder; xanthan gum; xanthophyll; ximenia americana seed oil; ximenia americana seed oil; ximenia americana seed oil; xylene; xylitol; xylityl caprate/caprylate; xylityl caprate/caprylate; xylityl cocoate; xylitylglucoside; xylose; yeast; yeast amino acids; yeast beta glucan; yeast extract; yeast ferment extract; yeast polysaccharides; yogurt; yogurt extract; yogurt powder; yucca aloifolia extract; yucca brevifolia powder; yucca brevifolia root extract; yucca filamentosa (spoonleaf yucca) extract; yucca filamentosa root; yucca glauca (soapweed) extract; yucca glauca (soapweed) root extract; yucca l. (yucca) root; yucca l. (yucca) root extract; yucca schidigera (mojave yucca); yucca schidigera (mojave yucca) extract; yucca schidigera fruit; yucca schidigera fruit juice; yucca vera (yucca) extract; zanthoxylum alatum; zanthoxylum alatum (winged prickly ash) extract; zanthoxylum americanum; zanthoxylum americanum (prickly ash) bark extract; zanthoxylum bungeanum extract; zanthoxylum piperitum fruit extract; zanthoxylum piperitum peel extract; zea mays (corn); zea mays (corn) cob powder; zea mays (corn) kernel extract; zea mays (corn) kernel meal; zea mays (corn) oil; zea mays (corn) seed flour; zea mays (corn) silk extract; zea mays (corn) starch; zein; zemea propanediol; zeolite; zeolite; zinax; zinc; zinc acetate; zinc acetylmethionate; zinc carbonate; zinc chloride; zinc citrate; zinc citrate trihydrate; zinc coceth sulfate; zinc gluconate; zinc lactate; zinc laurate; zinc myristate; zinc neodecanoate; zinc oxide; zinc oxide; zinc oxide(sunscreen grade); zinc oxide(sunscreen grade); zinc palmitate zinc palmitate; zinc pca; zinc phenolsulfonate; zinc pyrithione; zinc ricinoleate; zinc stearate; zinc sulfate; zinc sulfate monohydrate; zinc sulfide; zinc sulfide; zinc zeolite; zingiber cassumunar extract; zingiber officinale (ginger); zingiber officinale (ginger) extract; zingiber officinale (ginger) oil; zingiber officinale (ginger) root extract; zingiber officinale (ginger) root oil; zingiber officinale (ginger) root powder; zingiber officinale (ginger) water; zingiber zerumbet extract; ziziphus jujuba (jujube) extract; zizyphus joazeiro bark extract; zizyphus jujuba (jujube); zizyphus jujuba (jujube) fruit extract; zizyphus jujuba (jujube) fruit extract; zostera marina extract; zymomonas ferment extract"
    l=ingredients_list.split(";")
    for i in range(0,len(l),80):
        string=";".join(l[i:i+80])
        generated_output = generate_data(string)
        if generated_output:
            print("Generated Output:\n", generated_output)
