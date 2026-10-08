"""Hausa field-guide text, mirroring the English entries in disease_guide.py.

Scientific names stay in Latin. English disease names are kept in brackets so
extension officers can match them to printed material.
"""

from __future__ import annotations

DISEASE_GUIDE_HA = {
    "Tomato_Bacterial_canker": {
        "name": "Kansar Ƙwayoyin Cuta (Bacterial Canker)",
        "agent_type": "Ƙwayar cuta (bakteriya)",
        "agent": "Clavibacter michiganensis subsp. michiganensis",
        "summary": (
            "Cutar ƙwayoyin cuta ce da ke yaɗuwa cikin dukan shuka, tana sa shuka ta yi "
            "yaushi, kuma tana barin raunuka a jikin kara. Tana yaɗuwa cikin sauƙi ta "
            "kayan aiki, hannaye da iri."
        ),
        "traits": [
            "Ganyaye suna yin yaushi a gefe ɗaya na ganye ko gefe ɗaya na shuka",
            "Gefen ganye yana yin rawaya zuwa ruwan ƙasa, kamar an ƙone shi",
            "Raunuka masu tasowa, masu launin ruwan ƙasa mai haske a jikin kara; tsakiyar kara na iya yin rawaya ko ya zama rami",
            "Ƙananan ɗigo masu tasowa a jikin 'ya'yan itace da farin zobe a kewaye (“idon tsuntsu”)",
            "Idan aka yanka kara, hanyoyin ruwa a ciki sukan yi rawaya-ruwan ƙasa",
        ],
        "prevention": [
            "Fara da ingantaccen iri marar cuta da shukokin dashe masu lafiya",
            "Kada ka adana iri daga gonar da ta kamu da cuta",
            "Wanke wuƙaƙe, sanduna da hannaye tsakanin shuka da shuka (misali giya kashi 70% ko bilic kashi 0.5%, sannan a kurkura)",
            "Kada ka yi aiki a gona lokacin da ganyaye suke da ruwa",
            "Cire shukokin da suka kamu sosai ka lalata su; kada ka sa su a takin gargajiya",
            "Kada ka shuka tumatir, barkono ko danginsu a wurin har shekara 2–3",
        ],
    },
    "Tomato_Bacterial_spot": {
        "name": "Ɗigon Ƙwayoyin Cuta (Bacterial Spot)",
        "agent_type": "Ƙwayar cuta (bakteriya)",
        "agent": "Xanthomonas species (often X. euvesicatoria / X. vesicatoria / X. perforans)",
        "summary": (
            "Cutar ɗigo ce ta ganye da 'ya'yan itace da ta zama ruwan dare a lokacin damina. "
            "Fantsamar ruwa, iska da kayan aiki suna kai ƙwayoyin cutar daga shuka zuwa shuka."
        ),
        "traits": [
            "Ƙananan ɗigo masu duhu, masu kama da jiƙaƙƙe a jikin ganye, sau da yawa masu kusurwa",
            "Ɗigon na iya samun zoben rawaya, kuma idan sun bushe sukan bar ƙananan ramuka",
            "Idan cutar ta yi tsanani, ganyayen ƙasa suna yin rawaya su faɗi",
            "Ɗigo masu tasowa kamar ɓawon gyambo a jikin ɗanyen 'ya'yan itace; raunin ba ya shiga ciki sosai",
            "Tana ƙaruwa bayan ruwan sama, ban ruwa ta sama, ko ganyaye masu cunkoso da danshi",
        ],
        "prevention": [
            "Yi amfani da iri mai tsabta da irin da ke jure cuta idan akwai",
            "Zuba ruwa a gindin shuka; kada ka yayyafa ruwa ta sama da yamma",
            "Bar tazara tsakanin shuka don iska ta ratsa; ɗaure shuka a sanda don ganyaye kada su taɓa ƙasa",
            "Kada ka taɓa shuka mai ruwa; wanke kayan aiki bayan aiki a layin da ke da cuta",
            "Cire tumatir da suka tsiro da kansu da ragowar amfanin gona bayan girbi",
            "Yi jujjuyawa da hatsi ko kayan lambu masu ƙwaya (legumes) har shekara 2–3",
        ],
    },
    "Tomato_Early_blight": {
        "name": "Ƙonewar Ganye ta Farko (Early Blight)",
        "agent_type": "Naman gwari (fungus)",
        "agent": "Alternaria linariae (syn. Alternaria solani)",
        "summary": (
            "Cutar naman gwari ce da yawanci take farawa daga tsofaffin ganyaye. Zafi, "
            "danshin ganye da wahalar shuka suna ƙara ta."
        ),
        "traits": [
            "Ɗigo masu launin ruwan ƙasa da zobba a cikin juna (kamar allon harbi)",
            "Rawaya a kewayen ɗigon; ganyayen ƙasa ne suke fara mutuwa",
            "Raunuka na iya bayyana a jikin kara (ruɓewar wuya a ƙananan shuka) da kafaɗar 'ya'yan itace",
            "Faɗuwar ganyaye tana bar 'ya'yan itace a fili rana ta ƙona su",
            "Sau da yawa tana ƙaruwa a shukokin da ba su da isasshen taki (nitrogen) ko ruwa",
        ],
        "prevention": [
            "Rufe ƙasa da ciyawa (mulch) don rage fantsamar ƙwayoyin cuta zuwa ganye",
            "Ɗaure shuka a sanda ka yanke ganyayen ƙasa da ke taɓa ƙasa",
            "Zuba ruwa a gindin shuka da safe don ganyaye su bushe da wuri",
            "Kiyaye ƙarfin shuka da daidaitaccen taki; kada ka bar ta ta sha wahalar fari",
            "Cire ganyayen da suka kamu ka lalata ragowar amfanin gona bayan girbi",
            "Kada ka shuka tumatir ko dankalin turawa a wurin har shekara 2–3",
        ],
    },
    "Tomato_Late_blight": {
        "name": "Ƙonewar Ganye ta Ƙarshe (Late Blight)",
        "agent_type": "Fumfunar ruwa (oomycete)",
        "agent": "Phytophthora infestans",
        "summary": (
            "Cuta ce mai saurin ɓarna a yanayin sanyi da danshi. Tana iya lalata ganyaye da "
            "'ya'yan itace cikin 'yan kwanaki, kuma tana kama dankalin turawa."
        ),
        "traits": [
            "Manyan tabo marasa siffa, masu kama da mai, launin kore-zaitun zuwa ruwan ƙasa a jikin ganye",
            "Farin fumfuna mai laushi a ƙarƙashin ganye lokacin danshi",
            "Kara na iya samun layuka masu duhu; shuka na iya faɗuwa da sauri",
            "Tabo masu ƙarfi, ruwan ƙasa, masu kama da mai a jikin ɗanyen 'ya'yan itace",
            "Tana yaɗuwa da sauri bayan ruwan sama, hazo ko raɓa mai yawa",
        ],
        "prevention": [
            "Lalata tumatir da dankalin turawa da suka tsiro da kansu a kewayen gona",
            "Guji ban ruwa ta sama; kiyaye ganyaye a bushe gwargwadon iko",
            "Kada ka shuka tumatir kusa da dankalin turawa",
            "Cire shukokin da suka lalace sosai nan take ka saka su a buhu",
            "Yi amfani da irin da ke jure cuta idan ana sayar da su a yankinku",
            "Feshin kofa (copper) yana jinkirta cutar kawai; ba ya maye gurbin tsabta da bushewar ganye",
        ],
    },
    "Tomato_Leaf_mold": {
        "name": "Fumfunar Ganye (Leaf Mold)",
        "agent_type": "Naman gwari (fungus)",
        "agent": "Passalora fulva (syn. Cladosporium fulvum)",
        "summary": (
            "Cuta ce ta danshi, musamman a gidajen shuka (greenhouse) ko ganyaye masu cunkoso "
            "da danshi. Tana kama ganye ne galibi, ba 'ya'yan itace ba."
        ),
        "traits": [
            "Tabo masu launin kore mai haske zuwa rawaya a saman ganye",
            "Fumfuna mai laushi kamar karammiski, kore-zaitun zuwa toka-ruwan ƙasa, a ƙarƙashin waɗannan tabo",
            "Tsofaffin ganyaye ne suke fara kamuwa; idan ta tsananta sukan yi ruwan ƙasa su faɗi",
            "'Ya'yan itace ba sa yawan samun tabo, amma amfani yana raguwa yayin da ganyaye ke mutuwa",
            "Tana da alaƙa sosai da rashin iska da yawan danshi a iska",
        ],
        "prevention": [
            "Ƙara tazara ka yanke rassan da ba a so don iska ta ratsa amfanin gona",
            "Buɗe gidan shuka don iska; guji barin ganyaye da ruwa na dogon lokaci",
            "Zuba ruwa a ƙasa, ba a kan ganye ba",
            "Cire ganyayen da fumfuna ya yi wa yawa ka lalata su",
            "Zaɓi irin da ke jure fumfunar ganye idan ana noma a gidan shuka",
        ],
    },
    "Tomato_Mosaic_virus": {
        "name": "Cutar Mosaic (Mosaic Virus)",
        "agent_type": "Ƙwayar cuta ta virus",
        "agent": "Tomato mosaic virus (ToMV) ko Tobacco mosaic virus (TMV)",
        "summary": (
            "Ƙwayar cuta ce mai ƙarfi da ke rayuwa a cikin ragowar shuka, iri, da kuma a "
            "hannaye da kayan aiki. Babu maganin warkar da shuka a gona idan ta riga ta kamu."
        ),
        "traits": [
            "Gauraye ko tabo na kore mai haske da kore mai duhu a jikin ganye",
            "Ganyaye na iya zama kamar ganyen fern, su yi kunnuwa ko su yi sirara",
            "Shuka ta tsumbure, kuma 'ya'yan itace ba sa nuna daidai ko suna yin launin tagulla",
            "Alamomi sukan bayyana bayan taɓawa, yankewa ko dashe",
            "Ba ta fitar da fumfunar naman gwari ko ruwan ƙwayoyin cuta",
        ],
        "prevention": [
            "Sayi ingantaccen iri da aka gwada ba shi da virus; yi wa irin da ka adana maganin zafi kawai da hanyar da aka tabbatar",
            "Wanke hannaye da sabulu kafin yankewa; kada a sha taba a wurin renon shuka",
            "Wanke kayan aiki tsakanin shuka da shuka",
            "Cire shukokin da suka kamu da zarar alamun mosaic sun bayyana",
            "Kawar da ciyayi na dangin tumatir da ke iya ɗauke da virus",
            "Kada ka yi takin gargajiya da shukokin da suka kamu don amfani a wurin renon shuka na gaba",
        ],
    },
    "Tomato_Septoria_leaf_spot": {
        "name": "Ɗigon Ganye na Septoria (Septoria Leaf Spot)",
        "agent_type": "Naman gwari (fungus)",
        "agent": "Septoria lycopersici",
        "summary": (
            "Cutar ɗigon ganye ce ta lokacin damina da ke farawa daga ƙasan shuka ta haura "
            "sama, tana kakkaɓe ganyaye idan ba a kula ba."
        ),
        "traits": [
            "Ƙananan ɗigo masu zagaye da yawa (kimanin mm 2–5) masu iyaka mai duhu",
            "Tsakiya mai launin toka ko ruwan ƙasa mai haske; ƙananan baƙaƙen ɗigo na iya bayyana a tsakiya",
            "Ganyayen ƙasa ne suke fara yin rawaya su faɗi",
            "'Ya'yan itace ba sa yawan kamuwa, amma rana tana ƙona su idan ganyaye sun faɗi",
            "Fantsamar ƙasa da ruwan sama tana yaɗa ƙwayoyin cutar",
        ],
        "prevention": [
            "Rufe ƙasa da ciyawa ka ɗaure shuka don ruwan sama kada ya fantsamar da ƙasa zuwa ganye",
            "Cire ganyayen ƙasa da suka kamu ka lalata su",
            "Zuba ruwa a ƙasa da safe",
            "Guji ganyaye masu cunkoso da ba a yanke ba",
            "Kada ka shuka tumatir a wurin har shekara 2–3; binne ko cire tsofaffin shuka",
        ],
    },
    "Tomato_Spider_mites": {
        "name": "Ƙananan Ƙwari Masu Saƙa (Spider Mites)",
        "agent_type": "Ƙwaro mai ƙafa takwas (mite)",
        "agent": "Tetranychus urticae (two-spotted spider mite)",
        "summary": (
            "Ƙananan ƙwari ne da ke tsotse ruwan ganye, musamman a lokacin zafi, bushewa da "
            "ƙura. Ba naman gwari ba ne, ba ƙwayoyin cuta ba, kuma ba virus ba."
        ),
        "traits": [
            "Ƙananan ɗigo masu rawaya ko fari a saman ganye",
            "Ganyaye suna yin launin tagulla, su bushe, kuma suna iya faɗuwa",
            "Siririyar saƙar gizo a ƙarƙashin ganye idan sun yi yawa",
            "Ƙwarin suna kama da ƙura mai motsi a ƙarƙashin ganye (yi amfani da gilashin ƙara girma)",
            "Suna ƙaruwa a shukokin da ke jin ƙishirwa da layukan da ke da ƙura",
        ],
        "prevention": [
            "Ba shuka isasshen ruwa; ganyaye masu ƙura da fari suna sa ƙwarin su yawaita",
            "Guji magungunan kashe ƙwari masu kashe komai da ke kashe abokan gaban waɗannan ƙwari",
            "A ƙananan gonaki, fesa ƙarƙashin ganye da ruwa mai ƙarfi",
            "Kawo ko kiyaye ƙwari masu cin waɗannan ƙwari (predatory mites) idan akwai",
            "Cire ganyayen ƙasa da suka cika da ƙwari ka lalata su",
            "Kawar da ciyayin da ke ɗauke da ƙwarin a kewayen gona",
        ],
    },
    "Tomato_Target_spot": {
        "name": "Ɗigon Zobe (Target Spot)",
        "agent_type": "Naman gwari (fungus)",
        "agent": "Corynespora cassiicola",
        "summary": (
            "Cutar naman gwari ce ta ɗigon ganye da 'ya'yan itace wadda zafi da danshi ke "
            "ƙara ta. Raunukan sukan nuna zobba, kamar ƙonewar ganye ta farko."
        ),
        "traits": [
            "Ɗigo masu ruwan ƙasa, masu zagaye ko marasa siffa, sau da yawa da zobba a cikin juna",
            "Tsakiya na iya tsagewa ko ta faɗi; zoben rawaya ya zama ruwan dare",
            "Tana iya kaiwa kara da 'ya'yan itace a matsayin raunuka masu ruwan ƙasa da suka ɗan nutse",
            "Ganyayen ƙasa da na cikin shuka ne suke fara kamuwa",
            "Yawan danshi da daɗewar ganye da ruwa suna gaggauta yaɗuwarta",
        ],
        "prevention": [
            "Inganta iska: ɗaure shuka, yanke rassa, kuma guji cunkoso",
            "Rufe ƙasa da ciyawa, ka yi ban ruwa na ɗigo ko na kwami maimakon ta sama",
            "Cire ganyayen da suka kamu da ragowar amfanin gona",
            "Kada ka shuka a gonar da ta yi fama da wannan cuta a tumatir ko kokwamba kwanan nan",
            "Yi jujjuyawar amfanin gona na shekara 2–3 da amfanin gonar da cutar ba ta kamawa",
        ],
    },
    "Tomato_Yellow_Leaf_Curl_Virus": {
        "name": "Cutar Naɗewar Ganye da Rawaya (Yellow Leaf Curl Virus)",
        "agent_type": "Ƙwayar cuta ta virus",
        "agent": "Tomato yellow leaf curl virus (TYLCV), wanda farin ƙuda (Bemisia tabaci) ke yaɗawa",
        "summary": (
            "Virus ce da farin ƙuda ke yaɗawa. Feshin maganin naman gwari a ganye ba ya "
            "warkar da shuka; dole ne a magance farin ƙuda da shukokin da suka kamu."
        ),
        "traits": [
            "Ganyaye matasa suna naɗewa ko lanƙwasawa zuwa sama",
            "Rawaya mai ƙarfi tsakanin jijiyoyin ganye; ganyaye suna ƙanƙancewa su yi kauri",
            "Shuka ta tsumbure sosai; furanni kaɗan ne ke ba da 'ya'ya",
            "'Ya'yan itacen da suka fito ƙanana ne; shuka tana kama da an tattara ta a sama",
            "Farin ƙuda (ƙananan ƙwari farare) sukan kasance a ƙarƙashin ganye",
        ],
        "prevention": [
            "Yi amfani da irin da ke jure TYLCV idan ana sayar da shi a kasuwarku",
            "Kare wurin renon shuka da raga mai hana ƙwari shiga",
            "Cire shukokin da ke da naɗewa da rawaya da zarar sun bayyana",
            "Magance farin ƙuda da tarkon rawaya mai ɗanko, ciyawar rufe ƙasa mai haskaka rana, da magungunan da aka amince da su ana sauyawa",
            "Kawar da ciyayi da tumatir da suka tsiro da kansu da ke ɗauke da farin ƙuda",
            "Kada ka yi dashe daga wurin renon shuka mai farin ƙuda zuwa gona mai tsabta",
        ],
    },
    "Tomato_healthy": {
        "name": "Ganye Mai Lafiya (Healthy)",
        "agent_type": "Babu",
        "agent": "Ba a gano wani mai haddasa cuta a wannan hoton ganye ba",
        "summary": (
            "Siffar ganyen ta yi daidai da ganyen tumatir mai lafiya. Ci gaba da kula da gona "
            "yadda aka saba don shuka su kasance da tsabta."
        ),
        "traits": [
            "Launin kore daidai ba tare da gauraye, zoben rawaya ko tabo masu kama da mai ba",
            "Babu zobba a cikin juna, ƙananan ramuka, ko fumfuna mai laushi a ƙarƙashin ganye",
            "Gefen ganye bai ƙone ba kuma bai naɗe sosai ba",
            "Babu saƙar gizo ko ɗigo masu yawa",
        ],
        "prevention": [
            "Ci gaba da duba ganyayen ƙasa bayan ruwan sama; cire ganyayen farko da suka kamu",
            "Zuba ruwa a ƙasa, ba a kan ganye ba, kuma ka bar tazara don shuka su bushe",
            "Yi amfani da iri mai tsabta, kayan aiki masu tsabta, da jujjuyawar amfanin gona ta shekara 2–3",
            "Magance farin ƙuda da ƙananan ƙwari da wuri don kada virus da ɗigo su yawaita",
            "Lalata ragowar amfanin gona a ƙarshen kakar noma",
        ],
    },
}
