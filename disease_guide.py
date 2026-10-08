"""Field-guide text shown after a HORTIVISION-NG prediction."""

from __future__ import annotations

DISEASE_GUIDE = {
    "Tomato_Bacterial_canker": {
        "name": "Bacterial Canker",
        "agent_type": "Bacterium",
        "agent": "Clavibacter michiganensis subsp. michiganensis",
        "summary": (
            "A systemic bacterial disease that can wilt whole plants and leave "
            "open cankers on stems. It spreads easily on tools, hands, and seed."
        ),
        "traits": [
            "Wilting of leaflets on one side of a leaf or one side of the plant",
            "Yellow to brown leaf margins with a dull, scorched look",
            "Raised, light-brown cankers on stems; pith may be yellow or hollow",
            "Small raised spots on fruit with a white halo (“bird’s-eye” spots)",
            "Vascular tissue in a cut stem often appears yellow-brown",
        ],
        "prevention": [
            "Start with certified disease-free seed and healthy transplants",
            "Do not save seed from infected fields",
            "Disinfect knives, stakes, and hands between plants (e.g. 70% alcohol or 0.5% bleach, then rinse)",
            "Avoid working the crop when leaves are wet",
            "Remove and destroy severely infected plants; do not compost them",
            "Rotate out of tomato, pepper, and related crops for at least 2–3 years",
        ],
    },
    "Tomato_Bacterial_spot": {
        "name": "Bacterial Spot",
        "agent_type": "Bacterium",
        "agent": "Xanthomonas species (often X. euvesicatoria / X. vesicatoria / X. perforans)",
        "summary": (
            "A common wet-weather leaf and fruit spot. Splash, wind, and tools "
            "move bacteria from plant to plant."
        ),
        "traits": [
            "Small, dark, water-soaked spots on leaves, often angular",
            "Spots may have a yellow halo and can dry out, leaving shot-holes",
            "Heavy infection yellows and drops lower leaves",
            "Raised, scabby spots on green fruit; lesions stay superficial",
            "Worse after rain, overhead irrigation, or dense, humid canopies",
        ],
        "prevention": [
            "Use clean seed and resistant varieties where available",
            "Water at the soil line; avoid overhead sprinkling in the evening",
            "Space plants for airflow; stake or trellis to keep foliage off the ground",
            "Do not touch wet plants; clean tools after working a sick row",
            "Remove volunteer tomatoes and crop debris after harvest",
            "Rotate with cereals or legumes for 2–3 years",
        ],
    },
    "Tomato_Early_blight": {
        "name": "Early Blight",
        "agent_type": "Fungus",
        "agent": "Alternaria linariae (syn. Alternaria solani)",
        "summary": (
            "A fungal blight that usually starts on older leaves. It is favoured "
            "by warm weather, leaf wetness, and plant stress."
        ),
        "traits": [
            "Brown spots with concentric rings (“target” or “bull’s-eye” pattern)",
            "Yellowing around the spots; lower leaves die first",
            "Lesions may appear on stems (collar rot on seedlings) and fruit shoulders",
            "Defoliation exposes fruit to sunscald",
            "Often worse on plants short of nitrogen or water",
        ],
        "prevention": [
            "Mulch soil to reduce splash of spores onto leaves",
            "Stake plants and prune lower leaves that touch the soil",
            "Water the base of the plant in the morning so foliage dries quickly",
            "Keep plants vigorous with balanced fertiliser; avoid drought stress",
            "Remove infected leaves and destroy crop residue after harvest",
            "Rotate away from tomato and potato for 2–3 years",
        ],
    },
    "Tomato_Late_blight": {
        "name": "Late Blight",
        "agent_type": "Oomycete (water mould)",
        "agent": "Phytophthora infestans",
        "summary": (
            "A fast, destructive blight in cool, wet weather. It can ruin foliage "
            "and fruit in a few days and also attacks potato."
        ),
        "traits": [
            "Large, irregular, greasy olive-to-brown patches on leaves",
            "White, downy growth on the underside of leaves in humid weather",
            "Stems may show dark brown streaks; plants can collapse quickly",
            "Firm, brown, greasy blotches on green fruit",
            "Spreads rapidly after rain, fog, or heavy dew",
        ],
        "prevention": [
            "Destroy volunteer tomato and potato plants around the field",
            "Avoid overhead irrigation; keep the canopy as dry as possible",
            "Do not plant tomato next to potato",
            "Remove and bag badly blighted plants immediately",
            "Use resistant cultivars if they are sold locally",
            "Copper sprays only delay it; they do not replace sanitation and dry foliage",
        ],
    },
    "Tomato_Leaf_mold": {
        "name": "Leaf Mold",
        "agent_type": "Fungus",
        "agent": "Passalora fulva (syn. Cladosporium fulvum)",
        "summary": (
            "A humidity disease, especially in greenhouses or crowded wet canopies. "
            "It mainly attacks leaves, not fruit."
        ),
        "traits": [
            "Pale green to yellow patches on the upper leaf surface",
            "Olive-green to grey-brown velvety mould on the underside of those patches",
            "Older leaves are hit first; severe cases brown and drop",
            "Fruit is usually not spotted, but yield falls as leaves die",
            "Strongly linked to poor airflow and high relative humidity",
        ],
        "prevention": [
            "Increase spacing and prune suckers so air moves through the crop",
            "Vent greenhouses; avoid prolonged leaf wetness",
            "Water the soil, not the leaves",
            "Remove and destroy badly moulded leaves",
            "Choose leaf-mold-resistant varieties for protected culture",
        ],
    },
    "Tomato_Mosaic_virus": {
        "name": "Mosaic Virus",
        "agent_type": "Virus",
        "agent": "Tomato mosaic virus (ToMV) or Tobacco mosaic virus (TMV)",
        "summary": (
            "A stable virus that survives in debris, seed, and on hands and tools. "
            "There is no field cure once a plant is infected."
        ),
        "traits": [
            "Light- and dark-green mosaic or mottling on leaves",
            "Leaves may be fern-like, puckered, or narrowed",
            "Stunted plants with uneven fruit ripening or bronzing",
            "Symptoms often appear after handling, pruning, or transplanting",
            "Does not produce fungal mould or bacterial ooze",
        ],
        "prevention": [
            "Buy certified virus-tested seed; heat-treat farm-saved seed only with a proven protocol",
            "Wash hands with soap before pruning; do not smoke tobacco in the nursery",
            "Disinfect tools between plants",
            "Rogue infected plants as soon as mosaic is obvious",
            "Control weeds in the tomato family that can harbour the virus",
            "Do not compost infected vines into the next nursery mix",
        ],
    },
    "Tomato_Septoria_leaf_spot": {
        "name": "Septoria Leaf Spot",
        "agent_type": "Fungus",
        "agent": "Septoria lycopersici",
        "summary": (
            "A wet-season leaf spot that starts at the bottom of the plant and "
            "climbs upward, stripping leaves if ignored."
        ),
        "traits": [
            "Many small circular spots (about 2–5 mm) with dark borders",
            "Grey or tan centres; tiny black dots (pycnidia) may be visible in the centre",
            "Yellowing and drop of lower leaves first",
            "Fruit is rarely infected, but exposed fruit sunburns after defoliation",
            "Splash from soil and rain spreads spores",
        ],
        "prevention": [
            "Mulch and stake so rain does not splash soil onto leaves",
            "Strip the lowest infected leaves and destroy them",
            "Water at ground level in the morning",
            "Avoid dense, unpruned canopies",
            "Rotate out of tomato for 2–3 years; bury or remove old vines",
        ],
    },
    "Tomato_Spider_mites": {
        "name": "Two-Spotted Spider Mites",
        "agent_type": "Arachnid pest (mite)",
        "agent": "Tetranychus urticae (two-spotted spider mite)",
        "summary": (
            "Tiny mites that suck leaf sap, especially in hot, dry, dusty weather. "
            "They are not a fungus, bacterium, or virus."
        ),
        "traits": [
            "Fine yellow or white stippling on the upper leaf surface",
            "Leaves turn bronze, dry, and may drop",
            "Fine silk webbing on the underside of leaves in heavy infestations",
            "Mites look like moving dust specks on the underside (use a hand lens)",
            "Worse on water-stressed plants and in dusty rows",
        ],
        "prevention": [
            "Keep plants watered; dusty, drought-stressed canopies explode with mites",
            "Avoid unnecessary broad-spectrum insecticides that kill mite predators",
            "Hose the underside of leaves with a strong water jet in small plots",
            "Introduce or conserve predatory mites where available",
            "Remove heavily infested lower leaves and destroy them",
            "Control weeds that host mites around the field",
        ],
    },
    "Tomato_Target_spot": {
        "name": "Target Spot",
        "agent_type": "Fungus",
        "agent": "Corynespora cassiicola",
        "summary": (
            "A fungal leaf and fruit spot favoured by warm, humid conditions. "
            "Lesions often show rings, similar to early blight."
        ),
        "traits": [
            "Brown circular to irregular spots, often with concentric rings",
            "Centres may crack or fall out; a yellow halo is common",
            "Can move onto stems and onto fruit as slightly sunken brown lesions",
            "Lower and inner canopy leaves are affected first",
            "High humidity and long leaf wetness speed the epidemic",
        ],
        "prevention": [
            "Improve airflow: stake, prune, and avoid overcrowding",
            "Mulch and drip or basin irrigation instead of overhead watering",
            "Remove infected leaves and crop debris",
            "Do not plant into fields with a recent history of target spot on tomato or cucumber",
            "Keep a 2–3 year rotation with non-host crops",
        ],
    },
    "Tomato_Yellow_Leaf_Curl_Virus": {
        "name": "Yellow Leaf Curl Virus",
        "agent_type": "Virus",
        "agent": "Tomato yellow leaf curl virus (TYLCV), spread by whiteflies (Bemisia tabaci)",
        "summary": (
            "A whitefly-borne virus. The plant is not cured by spraying the leaves "
            "with fungicide; you must manage whiteflies and infected plants."
        ),
        "traits": [
            "Upward cupping or curling of young leaves",
            "Strong yellowing between veins; leaves become small and thickened",
            "Severe stunting; few flowers set fruit",
            "Fruit that forms is small; plants look bunched at the top",
            "Whiteflies (tiny white insects) often present on the underside of leaves",
        ],
        "prevention": [
            "Use TYLCV-resistant or tolerant varieties if sold in your market",
            "Protect nurseries with insect-proof netting",
            "Rogue plants with curl and yellowing as soon as they appear",
            "Control whiteflies with yellow sticky traps, reflective mulch, and approved insecticides in rotation",
            "Remove weeds and volunteer tomatoes that host whiteflies",
            "Do not transplant from an infested nursery into a clean field",
        ],
    },
    "Tomato_healthy": {
        "name": "Healthy leaf",
        "agent_type": "None",
        "agent": "No disease agent detected on this leaf image",
        "summary": (
            "The leaf pattern matches a healthy tomato leaflet. Continue ordinary "
            "crop care so the stand stays clean."
        ),
        "traits": [
            "Even green colour without mottling, yellow halos, or greasy patches",
            "No concentric rings, shot-holes, or velvety mould on the underside",
            "Leaf edges not scorched or strongly cupped",
            "No silk webbing or heavy stippling",
        ],
        "prevention": [
            "Keep inspecting lower leaves after rain; remove the first diseased leaflets",
            "Water the soil, not the foliage, and give plants space to dry",
            "Use clean seed, clean tools, and a 2–3 year rotation",
            "Control whiteflies and mites early so viruses and stippling do not build up",
            "Destroy crop residue at the end of the season",
        ],
    },
}


def get_guide(class_key: str, lang: str = "en") -> dict:
    if lang == "ha":
        from disease_guide_ha import DISEASE_GUIDE_HA

        if class_key in DISEASE_GUIDE_HA:
            return DISEASE_GUIDE_HA[class_key]
    if class_key in DISEASE_GUIDE:
        return DISEASE_GUIDE[class_key]
    return {
        "name": class_key.replace("_", " "),
        "agent_type": "Unknown",
        "agent": "Not listed in the field guide",
        "summary": "No local advisory text is stored for this class.",
        "traits": [],
        "prevention": [],
    }
