import random

# Mianownik 	M. 	kto? co? (jest) 	            góra 	słońce 	wiatr
# Dopełniacz 	D. 	kogo? czego? (nie ma) 	        góry 	słońca 	wiatru
# Celownik      C. 	komu? czemu? (się przyglądam) 	górze 	słońcu 	wiatrowi
# Biernik 	    B. 	kogo? co? (widzę) 	            górę 	słońce 	wiatr
# Narzędnik  	N. 	(z) kim? (z) czym? (idę) 	    (z) górą 	(ze) słońcem 	(z) wiatrem
# Miejscownik 	Ms. o kim? o czym? (mówię) 	        (o) górze 	(o) słońcu 	(o) wietrze
# Wołacz 	    W. 	zwrot do kogoś lub czegoś 	    góro 	słońce 	wietrze 

def case_name_to_index(case):
    return {
        "nominative": 0,
        "genitive": 1,
        "dative": 2,
        "accusative": 3,
        "instrumental": 4,
        "locative": 5,
        "vocative": 6,

        "mianownik": 0,
        "dopełniacz": 1,
        "dopelniacz": 1,
        "celownik": 2,
        "biernik": 3,
        "narzędnik": 4,
        "narzednik": 4,
        "miejscownik": 5,
        "wołacz": 6,
        "wolacz": 6
    }[case]

def get_random_nickname(message, case, cmd=None):
    nicks = None

    if message.server and message.server.id == "318733700160290826":
        nicks = nicks_default + nicks_mpf
    elif message.server and message.server.id == "174449535811190785":
        nicks = nicks_default + nicks_politbiuro
    else:
        nicks = nicks_default + nicks_politbiuro
    
    index = random.randint(0, len(nicks)-1)

    if cmd and (0 <= index <= len(nicks_default)-1):
        ret = None
        if cmd == ".czyim":
            ret = ["moim", "twoim", "niczyim"]
        if cmd == ".czyimi":
            ret = ["moimi", "twoimi", "niczyimi"]
        if cmd == ".czyich":
            ret = ["moich", "twoich", "niczyich"]
        elif cmd == ".czyja":
            ret = ["moja", "twoja", "niczyja"]
        elif cmd == ".czyje":
            ret = ["moje", "twoje", "niczyje"]
        elif cmd == ".czyją":
            ret = ["moją", "twoją", "niczyją"]
        elif cmd == ".czyj":
            ret = ["mój", "twój", "niczyj"]
        elif cmd == ".czyjego":
            ret = ["mojego", "twojego", "niczyjego"]
        elif cmd == ".czyjej":
            ret = ["mojej", "twójej", "niczyjej"]
        
        return ret[index]
    else:
        return nicks[index][case_name_to_index(case)]


nicks_default = [
    ["ja", "mnie", "mi", "mnie", "mną", "mnie", "ja"],
    ["ty", "ciebie", "tobie", "ciebie", "tobą", "tobie", "ty"],
    ["nikt", "nikogo", "nikomu", "nikogo", "nikim", "nikim", "nikt"]
]

nicks_politbiuro = [
    ["8azyliszek", "8azyliszka", "8azyliszkowi", "8azyliszka", "8azyliszkiem", "8azyliszku", "8azyli"],
    ["Abyss", "Abyssie", "Abyssowi", "Abyssa", "Abyssem", "Abyssie", "Abyss"],
    ["Accoun", "Accouna", "Accounowi", "Accouna", "Accounem", "Accounie", "Accoun"],
    ["Aiden", "Aidena", "Aidenowi", "Aidena", "Aidenem", "Aidenie", "Aiden"],
    ["Artius", "Artiusa", "Artiusowi", "Artiusa", "Artiusem", "Artiusie", "Artiusie"],
    ["b3rt", "b3rta", "b3rtowi", "b3rta", "b3rtem", "b3rcie", "b3rt"],
    ["Behe", "Behego", "Behemu", "Behego", "Behem", "Behe", "Behe"],
    ["Berlin", "Berlina", "Berlinowi", "Berlina", "Berlinem", "Berlinie", "Berlinie"],
    ["Bethezer", "Bethezera", "Bethezerowi", "Bethezera", "Bethezerem", "Bethezerze", "Beth"],
    ["Black Shadow", "Blacka", "Blackowi", "Blacka", "Blackiem", "Blacku", "Black"],
    ["Bryl", "Bryla", "Brylowi", "Bryla", "Brylem", "Brylu", "Brylu"],
    ["Cardi", "Cardiego", "Cardiemu", "Cardiego", "Cardiem", "Cardim", "Cardi"],
    ["CormaC <:komarcz:328946510274232330>", "CormaCa <:komarcz:328946510274232330>", "CormaCowi <:komarcz:328946510274232330>", "CormaCa <:komarcz:328946510274232330>", "CormaCem <:komarcz:328946510274232330>", "CormaCu <:komarcz:328946510274232330>", "CormaC <:komarcz:328946510274232330>"],
    ["Debiru", "Debira", "Debirowi", "Debira", "Debirem", "Debiru", "Debiru"],
    ["deffik", "deffika", "deffikowi", "deffika", "deffikiem", "deffiku", "deffiku"],
    ["Devius", "Deviusa", "Deviusowi", "Deviusa", "Deviusem", "Deviusie", "Deviusie"],
    ["Dracia", "Dracii", "Dracii", "Dracię", "Dracią", "Dracii", "Dracia"],
 #   ["Elano", "Elana", "Elanowi", "Elana", "Elanem", "Elanie", "Elano"],
 #   ["emqi", "emqiego", "emqiemu", "emqiego", "emqim", "emqim", "emqi"],
    ["FaceDancer", "FaceDancera", "FaceDancerowi", "FaceDancera", "FaceDancerem", "FaceDancerze", "FaceDancer"],
    ["Fel", "Fela", "Felowi", "Fela", "Felem", "Felu", "Fel"],
    ["Germa", "Germy", "Germie", "Germę", "Germą", "Germie", "Germa"],
 #   ["gen", "gena", "genowi", "gena", "genem", "genie", "genie"],
    ["Gofer", "Gofra", "Gofrowi", "Gofra", "Gofrem", "Gofrze", "Gofrze"],
    ["grz", "grza", "grzowi", "grza", "grzem", "grze", "grz"],
    ["JamesVoo", "JamesaVoo", "JamesowiVoo", "JamesaVoo", "JamesemVoo", "JamesieVoo", "James"],
    ["Hakken", "Hakkena", "Hakkenowi", "Hakkena", "Hakkenem", "Hakkenie", "Hakken"],
    ["Holy.Death", "Holiego", "Holiemu", "Holiego", "Holim", "Holim", "Holy"],
    ["Hrabula", "Hrabuli", "Hrabuli", "Hrabulę", "Hrabulą", "Hrabuli", "Hrabula"],
    ["Kath", "Kath", "Kath", "Kath", "Kath", "Kath", "Kath"],
    ["kicek", "kicka", "kickowi", "kicka", "kickiem", "kicku", "kicku"],
    ["Knight Martius", "Martiusa", "Martiusowi", "Martiusa", "Martiusem", "Martiusie", "Martiusie"],
    ["Lord Nargogh", "Nargogha", "Nargoghowi", "Nargogha", "Nargoghiem", "Nargoghu", "Nargogh"],
    ["orgiełe", "orgieła", "orgiełemu", "orgieła", "orgiełem", "orgiełe", "orgu"],
    ["opti", "optiego", "optiemu", "optiego", "optim", "optim", "opti"],
    ["MSaint", "MSainta", "MSaintowi", "MSainta", "MSaintem", "MSaincie", "MSaincie"],
    ["Mav", "Mavcia", "Mavciowi", "Mavcia", "Mavciem", "Mavciu", "Mavciu"],
    ["Metalus", "Metalusa", "Metalusowi", "Metalusa", "Metalusem", "Metalusie", "Metalusie"],
 #   ["Murezor", "Murezora", "Murezorowi", "Murezora", "Murezorem", "Murezorze", "Murezorze"],
 #   ["Mysquff", "Mysquffa", "Mysquffowi", "Mysquffa", "Mysquffem", "Mysquffie", "Mysquff"],
    ["nerv0", "nerv4", "nerv0wi", "nerv4", "nerv3m", "nerv1e", "nerv0"],
    ["Niziołka", "Niziołki", "Niziołce", "Niziołkę", "Niziołką", "Niziołce", "Niziołka"],
    ["Noobirus", "Noobirusa", "Noobirusowi", "Noobirusa", "Noobirusem", "Noobirusie", "Noobirusie"],
    ["OAT", "OATa", "OATowi", "OATa", "OATem", "OATcie", "OAT"],
    ["Osioł", "Osła", "Osłu", "Osła", "Osłem", "Ośle", "Ośle"],
    ["P_aul", "P_aula", "P_aulowi", "P_aula", "P_aulem", "P_aulu", "P_"],
    ["Pałker", "Pałkera", "Pałkerowi", "Pałkera", "Pałkerem", "Pałkerze", "Pałker"],
    ["Pezet", "Pezeta", "Pezetowi", "Pezeta", "Pezetem", "Pezecie", "Pezet"],
    ["podbiel", "podbiela", "podbielowi", "podbiela", "podbielem", "podbielu", "podbielu"],
 #   ["POLIP", "POLIPa", "POLIPowi", "POLIPa", "POLIPem", "POLIPie", "POLIPie"],
    ["Princess Nue", "Nue", "Nue", "Nue", "Nuem", "Nue", "Nue"],
    ["Ramzes", "Ramzesa", "Ramzesowi", "Ramzesa", "Ramzesem", "Ramzesie", "Ramzesie"],
    ["rane", "rane", "rane", "rane", "rane", "rane", "rane obsrane i niepozmywane"],
 #   ["RIP", "RIPa", "RIPowi", "RIPa", "RIPem", "RIPie", "RIPie"],
    ["Rysia", "Rysi", "Rysi", "Rysi", "Rysią", "Rysi", "Rysiu"],
 #   ["Seeker", "Seekera", "Seekerowi", "Seekera", "Seekerem", "Seekerze", "Seekerze"],
    ["Sermaciej", "Sermacieja", "Sermaciejowi", "Sermacieja", "Sermaciejem", "Sermacieju", "Sermacieju"],
    ["Shaker", "Shakera", "Shakerowi", "Shakera", "Shakerem", "Shakerze", "Shaker"],
    ["Smuggler <:smaglor:328947669676457984>", "Smugglera <:smaglor:328947669676457984>", "Smugglerowi <:smaglor:328947669676457984>", "Smugglera <:smaglor:328947669676457984>", "Smugglerem <:smaglor:328947669676457984>", "Smugglerze <:smaglor:328947669676457984>", "Smugglerze <:smaglor:328947669676457984>"],
    ["Stefan", "Stefana", "Stefanowi", "Stefana", "Stefanem", "Stefanie", "Stefan"],
    ["Śćas", "Śćasa", "Śćasowi", "Śćasa", "Śćasem", "Śćasie", "Śćias"],
    ["t3tris", "t3trisa", "t3trisowi", "t3trisa", "t3trisem", "t3trisie", "t3tris"],
    ["Still", "Stilla", "Stillowi", "Stilla", "Stillem", "Stillu", "Still"],
    ["Teb", "Teba", "Tebowi", "Teba", "Tebem", "Tebie", "Teb"],
    ["Ture", "Tura", "Turowi", "Tura", "Turem", "Turze", "Turze"],
    ["Voda", "Vody", "Vodzie", "Vodę", "Vodą", "Vodzie", "Vodecki"],
    ["Xardas", "Xardasa", "Xardasowi", "Xardasa", "Xardasem", "Xardasie", "Xardasie"],
    ["Xerber", "Xerbera", "Xerberowi", "Xerbera", "Xerberem", "Xerberze", "Xerber"],
    ["Xysiu", "Xysia", "Xysiowi", "Xysia", "Xysiem", "Xysiu", "Xysiu"],
    ["yojec", "yojca", "yojcowi", "yojca", "yojcem", "yojcu", "yojcu"],
    ["ziom", "zioma", "ziomowi", "zioma", "ziomem", "ziomie", "ziom"]
]

nicks_mpf = [
    ["Drejk", "Drejka", "Drejkowi", "Drejka", "Drejkiem", "Drejku", "Drejk"],
    ["Kubojax", "Kubojaxa", "Kubojaxowi", "Kubojaxa", "Kubojaxem", "Kubojaxie", "Kubojaxie"],
    ["Lutor", "Lutora", "Lutorowi", "Lutora", "Lutorem", "Lutorze", "Lutor"],
    ["Pecet", "Peceta", "Pecetowi", "Peceta", "Pecetem", "Pececie", "Pec"],
    ["Phate", "Phate", "Phate", "Phate", "Phate", "Phate", "Phate"],
    ["Shadow", "Shadow", "Shadow", "Shadow", "Shadow", "Shadow", "Shadow"],
    ["Skajt", "Skajta", "Skajtowi", "Skajta", "Skajtem", "Skajcie", "Skajcie"],
    ["yojec", "yojca", "yojcowi", "yojca", "yojcem", "yojcu", "yojcu"]
]