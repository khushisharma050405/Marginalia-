"""Curriculum Concepts Knowledge Base for CBSE and ICSE (Class Nursery to 12th)
Provides direct, authentic, curriculum-verified answers for core questions and concepts
across Science, EVS, Social Science, Mathematics, English, Hindi, Sanskrit,
Computer Science, AI, Commerce, and Economics.
"""

from typing import Optional, Dict, Any, List

CURRICULUM_CONCEPTS: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. SCIENCE & EVS (Primary to Middle School: Classes 1 - 8)
    # =========================================================================
    {
        "id": "seeds_and_germination",
        "title": "Seeds, Germination & Dispersal",
        "subject": "Science",
        "classes": ["3", "4", "5", "6", "7", "8", "Foundation"],
        "triggers": [
            "seed", "seeds", "what is seed", "what is a seed", "parts of seed", "parts of a seed",
            "seed coat", "cotyledon", "cotyledons", "embryo", "germination", "conditions for germination",
            "how seeds disperse", "seed dispersal", "dispersal of seeds", "radicle", "plumule"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "A seed is the reproductive unit of a flowering plant that contains a baby plant (embryo) "
            "and stored food (cotyledons), enclosed inside a protective seed coat. Under favourable conditions "
            "of air (oxygen), water (moisture), and warmth (suitable temperature), the seed germinates into a young seedling."
        ),
        "steps": [
            ("1. Scientific Definition",
             "A seed develops from a fertilized ovule inside the plant ovary. It represents the dormant reproductive "
             "stage of spermatophyte (flowering) plants, containing everything required to grow into a new plant."),
            ("2. The Three Essential Parts of a Seed",
             "• Seed Coat (Testa): The tough outer protective skin that shields the embryo from drying out, physical damage, and bacterial invasion.\n"
             "• Cotyledon (Seed Leaf): The fleshy leaf-like structure containing stored food (starch and proteins) that nourishes the germinating embryo until it grows true green leaves to photosynthesise. (Monocots have 1 cotyledon, e.g. corn, wheat; Dicots have 2 cotyledons, e.g. gram, peas, beans).\n"
             "• Embryo (Baby Plant): Consists of the Radicle (which grows downward to form the primary root system) and Plumule (which grows upward into the shoot and leaves)."),
            ("3. Vital Conditions for Germination",
             "Seed germination requires three non-negotiable abiotic factors:\n"
             "1. Water (Moisture): Softens the tough seed coat and activates enzymes to break down stored starch into soluble sugars.\n"
             "2. Air (Oxygen): Essential for aerobic cellular respiration, providing energy (ATP) for rapid cell division in the embryo.\n"
             "3. Warmth (Optimum Temperature: 20°C–30°C): Provides ideal kinetic energy for biochemical enzymatic activity. (Note: Seeds do not need sunlight during initial germination, as the food is provided by cotyledons)."),
            ("4. Mechanisms of Seed Dispersal",
             "Dispersal prevents overcrowding and competition for sunlight, water, and soil minerals:\n"
             "• Wind: Lightweight seeds equipped with wings or fine parachutes (e.g. Dandelion, Cotton, Drumstick, Maple).\n"
             "• Water: Lightweight seeds with spongy, fibrous or waterproof coverings (e.g. Coconut, Lotus).\n"
             "• Animals & Humans: Seeds with hooks, spines, or stiff hairs that cling to fur or clothing (e.g. Burrs, Xanthium, Bidens), or edible fruits ingested with hard seeds excreted elsewhere (e.g. Guava, Berries, Tomato).\n"
             "• Explosive Mechanism (Bursting Pods): Pods dry up under sunlight, build tension, and suddenly burst open, catapulting seeds several feet away (e.g. Peas, Balsam, Lady's finger)."),
            ("5. Official Curriculum Verification",
             "Verified against NCERT Class 5 EVS Chapter 5: 'Seeds and Seeds' and Class 6 & 7 NCERT Science: 'Getting to Know Plants' & 'Reproduction in Plants'. (Formula & Concept Verified ✓)")
        ]
    },
    {
        "id": "photosynthesis",
        "title": "Photosynthesis in Plants",
        "subject": "Science",
        "classes": ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "photosynthesis", "what is photosynthesis", "define photosynthesis", "explain photosynthesis",
            "how plants make food", "equation for photosynthesis", "chlorophyll function", "stomata"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "Photosynthesis is the autotrophic process by which green plants synthesize glucose (food) "
            "from carbon dioxide (CO₂) and water (H₂O) using solar light energy trapped by chlorophyll, "
            "releasing oxygen (O₂) as a life-supporting byproduct."
        ),
        "steps": [
            ("1. Balanced Chemical Equation",
             "6CO₂ (Carbon Dioxide) + 6H₂O (Water) ──[Sunlight / Chlorophyll]──> C₆H₁₂O₆ (Glucose) + 6O₂ (Oxygen)"),
            ("2. Essential Raw Materials & Absorption",
             "• Carbon Dioxide (CO₂): Diffuses into leaves from the atmosphere through microscopic pore openings called Stomata.\n"
             "• Water (H₂O) & Minerals: Absorbed by root hair cells from the soil via osmosis and transported upward through Xylem vessels.\n"
             "• Solar Energy: Photons captured by the green pigment Chlorophyll located within plant Chloroplasts.\n"
             "• Chlorophyll: Traps sunlight and drives the photo-chemical breakdown of water."),
            ("3. Two Sequential Stages",
             "1. Light-Dependent Reactions (in Thylakoid membranes): Photolysis of water splits H₂O into hydrogen ions, electrons, and O₂ gas, synthesizing ATP and NADPH.\n"
             "2. Light-Independent Reactions / Calvin Cycle (in Stroma): CO₂ is fixed and reduced using ATP and NADPH into glucose (C₆H₁₂O₆)."),
            ("4. Fate of Synthesized Food",
             "Excess glucose is converted into insoluble Starch for storage in leaves, tubers, and seeds, or transported as Sucrose via Phloem tissues."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 7 Science Chapter 1: 'Nutrition in Plants' & Class 10 Biology: 'Life Processes'. (Formula & Concept Verified ✓)")
        ]
    },
    {
        "id": "water_cycle",
        "title": "The Water Cycle (Hydrological Cycle)",
        "subject": "Science",
        "classes": ["3", "4", "5", "6", "7", "8", "9"],
        "triggers": [
            "water cycle", "what is water cycle", "explain water cycle", "evaporation", "condensation",
            "precipitation", "transpiration", "hydrological cycle", "water vapor"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "The water cycle is the continuous, natural circulation of water on, above, and below Earth's surface "
            "through solar-driven phase transitions: Evaporation, Transpiration, Condensation, Precipitation, and Infiltration/Collection."
        ),
        "steps": [
            ("1. The Core Stages of the Cycle",
             "• 1. Evaporation: Solar heat converts liquid water from oceans, rivers, and lakes into invisible water vapor (gas) that rises into the atmosphere.\n"
             "• 2. Transpiration: Loss of excess water vapor from aerial plant surfaces (especially stomata) into the air.\n"
             "• 3. Condensation: As warm water vapor rises, it cools in the upper troposphere, condensing around microscopic dust nuclei into tiny liquid droplets that aggregate to form clouds and fog.\n"
             "• 4. Precipitation: When condensed cloud droplets grow too heavy to remain suspended in rising air currents, they fall under gravity as rain, snow, hail, or sleet.\n"
             "• 5. Collection & Infiltration: Rainwater flows into surface water bodies (runoff) and percolates deep into soil layers (seepage) to recharge groundwater aquifers."),
            ("2. Physical Driving Engine",
             "Solar radiation provides the thermal energy required for liquid-to-gas phase change (latent heat of vaporization), while Earth's gravity pulls precipitation down and drives river runoff."),
            ("3. Ecological Importance",
             "Maintains global climate equilibrium, purifies freshwater resources, delivers nutrients to terrestrial ecosystems, and regulates weather cycles."),
            ("4. Real-World Applications",
             "Rainwater harvesting, construction of check dams, and weather forecasting all model water cycle principles."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 5 EVS ('Every Drop Counts') & Class 6 Science ('Water: A Precious Resource'). (Formula & Concept Verified ✓)")
        ]
    },
    {
        "id": "mitochondria_powerhouse",
        "title": "Mitochondria: The Powerhouse of the Cell",
        "subject": "Science",
        "classes": ["6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "mitochondria", "mitochondrion", "powerhouse of the cell", "powerhouse of cell", "why is mitochondria called powerhouse", "why is the mitochondrion referred to as the powerhouse"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "Mitochondria are known as the 'Powerhouse of the Cell' because they generate most of the chemical energy "
            "needed by the cell in the form of ATP (Adenosine Triphosphate) through cellular respiration."
        ),
        "steps": [
            ("1. Scientific Definition & Biological Function",
             "Mitochondria are double-membraned cellular organelles responsible for aerobic respiration, breaking down glucose metabolites to synthesize ATP (Adenosine Triphosphate), the universal energy currency of living cells."),
            ("2. Structure of Mitochondrion",
             "• Outer Membrane: Smooth and permeable to small molecules.\n"
             "• Inner Membrane: Deeply folded into finger-like projections called cristae, which maximize the surface area for ATP-generating respiratory enzyme complexes.\n"
             "• Matrix: Dense fluid containing mitochondrial DNA and 70S ribosomes, making mitochondria semiautonomous."),
            ("3. Cellular Respiration & ATP Production",
             "Metabolites enter the Krebs cycle and electron transport chain inside cristae, generating ATP molecules that supply cellular metabolic energy."),
            ("4. Curriculum Verification",
             "Verified against NCERT Class 9 Science Chapter: 'The Fundamental Unit of Life'. (Formula & Concept Verified ✓)")
        ]
    },
    {
        "id": "cell_biology",
        "title": "The Cell: Structural and Functional Unit of Life",
        "subject": "Science",
        "classes": ["6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "what is cell", "what is a cell", "cell theory", "define cell", "structure of cell",
            "nucleus", "plant cell vs animal cell", "prokaryotic vs eukaryotic", "ribosome", "cell membrane",
            "cytoplasm", "chloroplast", "vacuole"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "A cell is the fundamental structural, functional, and biological unit of all living organisms. "
            "It is surrounded by a cell membrane, contains cytoplasm, genetic material (DNA), and specialized organelles "
            "that execute life-sustaining biochemical processes."
        ),
        "steps": [
            ("1. The Cell Theory (Schleiden, Schwann & Virchow)",
             "1. All living organisms are composed of one or more cells.\n"
             "2. The cell is the basic structural and functional unit of life.\n"
             "3. All cells arise from pre-existing cells through cell division ('Omnis cellula-e-cellula')."),
            ("2. Essential Organelles & Their Functions",
             "• Nucleus ('Control Center'): Houses chromosomes and genetic material (DNA), directing protein synthesis and cell division.\n"
             "• Mitochondria ('Powerhouse of the Cell'): Double-membraned organelle that carries out cellular respiration to produce energy packets in the form of ATP (Adenosine Triphosphate).\n"
             "• Ribosomes ('Protein Factories'): Synthesize vital functional and structural proteins.\n"
             "• Endoplasmic Reticulum (ER): RER (studded with ribosomes, protein folding) and SER (lipid/steroid synthesis, detoxification).\n"
             "• Golgi Apparatus: Packages, modifies, and sorts synthesized proteins and lipids into vesicles.\n"
             "• Lysosomes ('Suicide Bags'): Contain hydrolytic digestive enzymes that break down cellular debris and worn-out organelles.\n"
             "• Chloroplasts (in plant cells): Contain chlorophyll to carry out photosynthesis.\n"
             "• Vacuoles: Fluid-filled storage sacs; plants have one large central vacuole that maintains turgidity."),
            ("3. Plant Cell vs Animal Cell Differences",
             "• Plant Cells: Possess a rigid outer Cell Wall (cellulose), plastids/chloroplasts, and a large central vacuole.\n"
             "• Animal Cells: Lack cell walls and plastids; have small, scattered vacuoles and centrosomes/centrioles for cell division."),
            ("4. Prokaryotic vs Eukaryotic Cells",
             "• Prokaryotes (Bacteria, Blue-green algae): Lack a membrane-bound nucleus and membrane-bound organelles (DNA in nucleoid region).\n"
             "• Eukaryotes (Plants, Animals, Fungi, Protists): Have a true membrane-bound nucleus and complex compartmentalized organelles."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 8 Science Chapter 8 & Class 9 Biology Chapter 5: 'The Fundamental Unit of Life'. (Formula & Concept Verified ✓)")
        ]
    },
    {
        "id": "friction",
        "title": "Friction and Its Laws",
        "subject": "Science",
        "classes": ["6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "friction", "what is friction", "types of friction", "static friction", "sliding friction",
            "rolling friction", "advantages of friction", "disadvantages of friction", "reduce friction"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "Friction is the contact resistance force that opposes the relative motion or tendency of motion "
            "between two surfaces in physical contact. It acts parallel to the contact surfaces and opposite to the direction of motion."
        ),
        "steps": [
            ("1. Cause of Friction",
             "At microscopic scales, even polished surfaces possess peaks and valleys (irregularities). When two surfaces press together, these irregularities interlock, creating microscopic cold welds that require tangential force to overcome."),
            ("2. Types of Friction (Ranked by Magnitude)",
             "Static Friction (fs) > Sliding/Kinetic Friction (fk) > Rolling Friction (fr)\n"
             "• Static Friction: Opposes impending motion when force is applied but no motion occurs yet (maximum value is Limiting Friction).\n"
             "• Sliding Friction: Resistance experienced when one body slides over another.\n"
             "• Rolling Friction: Resistance experienced when a circular body (wheel, sphere) rolls over a surface. (Rolling friction is significantly lower than sliding, which is why ball bearings and wheels are used)."),
            ("3. Why Friction is a 'Necessary Evil'",
             "• Advantages: Enables humans to walk without slipping, allows vehicle braking, enables writing with pen/chalk, and holds nails in walls.\n"
             "• Disadvantages: Causes wear and tear of machine parts and shoes, dissipates valuable energy as unwanted heat, and reduces engine efficiency."),
            ("4. Methods to Increase or Reduce Friction",
             "• To Reduce: Applying lubricants (oil, grease, graphite), using ball bearings, streamlining aerodynamic bodies, polishing surfaces.\n"
             "• To Increase: Grooving automobile tires, treaded soles of athletic shoes, applying resin on gymnast hands, applying rough sand on icy tracks."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 8 Science Chapter 12: 'Friction' and Class 11 Physics: 'Laws of Motion'. (Formula & Concept Verified ✓)")
        ]
    },

    # =========================================================================
    # 2. SOCIAL SCIENCE (History, Civics, Geography: Classes 1 - 10)
    # =========================================================================
    {
        "id": "indian_constitution",
        "title": "The Constitution of India",
        "subject": "Social Science (SST)",
        "classes": ["5", "6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "constitution", "what is constitution", "indian constitution", "preamble", "fundamental rights",
            "father of indian constitution", "br ambedkar", "dr b r ambedkar", "constituent assembly",
            "republic day", "directive principles", "secularism", "federalism"
        ],
        "badge": "Curriculum Fact Verified ✓",
        "direct_answer": (
            "The Constitution of India is the supreme legal document of the nation, laying down the framework "
            "defining fundamental political code, structure, procedures, powers, and duties of government institutions, "
            "and setting out the fundamental rights and directive principles of citizens."
        ),
        "steps": [
            ("1. Historic Background & Drafting",
             "• Drafting Committee Chairman: Dr. Bhimrao Ramji Ambedkar (recognized as the chief architect and Father of the Indian Constitution).\n"
             "• Constituent Assembly President: Dr. Rajendra Prasad.\n"
             "• Time taken to draft: Exactly 2 years, 11 months, and 18 days.\n"
             "• Adoption: 26th November 1949 (celebrated as Constitution Day / Samvidhan Divas).\n"
             "• Enforcement: 26th January 1950 (commemorated annually as Republic Day)."),
            ("2. The Preamble (Guiding Soul of the Constitution)",
             "Declares India to be a SOVEREIGN, SOCIALIST, SECULAR, DEMOCRATIC, REPUBLIC, securing to all citizens:\n"
             "• JUSTICE: Social, economic, and political;\n"
             "• LIBERTY: Of thought, expression, belief, faith, and worship;\n"
             "• EQUALITY: Of status and of opportunity;\n"
             "• FRATERNITY: Assuring the dignity of the individual and the unity and integrity of the Nation."),
            ("3. Six Fundamental Rights (Part III, Articles 12-35)",
             "1. Right to Equality (Articles 14–18)\n"
             "2. Right to Freedom (Articles 19–22)\n"
             "3. Right against Exploitation (Articles 23–24)\n"
             "4. Right to Freedom of Religion (Articles 25–28)\n"
             "5. Cultural and Educational Rights (Articles 29–30)\n"
             "6. Right to Constitutional Remedies (Article 32 — declared by Dr. Ambedkar as the 'Heart and Soul' of the Constitution)."),
            ("4. Key Pillars: Federalism & Secularism",
             "• Federalism: Distribution of legislative powers between Central and State governments via Union List, State List, and Concurrent List.\n"
             "• Secularism: The State has no official religion; all faiths are treated with equal respect and protection (Sarva Dharma Sambhava)."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 8 Civics Chapter 1: 'The Indian Constitution' & Class 9 Political Science: 'Constitutional Design'. (Curriculum Fact Verified ✓)")
        ]
    },
    {
        "id": "democracy",
        "title": "Democracy and Its Principles",
        "subject": "Social Science (SST)",
        "classes": ["5", "6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "democracy", "what is democracy", "define democracy", "features of democracy",
            "universal adult franchise", "rule of law", "elections", "pillars of democracy"
        ],
        "badge": "Curriculum Fact Verified ✓",
        "direct_answer": (
            "Democracy is a system of government where the supreme power is vested in the people and exercised "
            "by them directly or through freely elected representatives under a free and fair electoral system. "
            "(Famous definition by Abraham Lincoln: 'Government of the people, by the people, for the people')."
        ),
        "steps": [
            ("1. Key Characteristics of a Modern Democracy",
             "• Free, Fair, and Regular Elections: Citizens have real choices to elect or change rulers without fear or coercion.\n"
             "• Universal Adult Franchise: Every adult citizen aged 18 or above holds one vote, and every vote has equal value ('One person, one vote, one value').\n"
             "• Rule of Law: All citizens, including government officials and leaders, are subject to the same law.\n"
             "• Constitutional Protection of Minority Rights: Majority decisions cannot override fundamental human rights of minorities."),
            ("2. The Three Organs of Democratic Governance",
             "1. Legislature: Formulates laws and represents public will (Parliament: Lok Sabha & Rajya Sabha; State Assemblies).\n"
             "2. Executive: Implements laws and runs government administration (President, Prime Minister, Council of Ministers, Civil Services).\n"
             "3. Judiciary: Interprets laws, protects constitutional rights, and settles disputes independently (Supreme Court, High Courts)."),
            ("3. Why Democracy is Preferred over Dictatorship / Monarchy",
             "• Enhances human dignity by treating all citizens as equal sovereign electors.\n"
             "• Promotes accountability and transparency in public governance.\n"
             "• Provides a peaceful institutional mechanism to resolve social and ethnic conflicts.\n"
             "• Allows room to correct political mistakes through open debate and elections."),
            ("4. Local Democratic Governance: Panchayati Raj",
             "Decentralised local self-government in India consists of 3 tiers: Gram Panchayat (village), Panchayat Samiti (block), and Zila Parishad (district)."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 9 Democratic Politics Chapter 1: 'What is Democracy? Why Democracy?'. (Curriculum Fact Verified ✓)")
        ]
    },

    # =========================================================================
    # 3. COMPUTATIONAL THINKING & AI (Classes 6 - 12)
    # =========================================================================
    {
        "id": "computational_thinking_pillars",
        "title": "The Four Pillars of Computational Thinking",
        "subject": "Computational Thinking & AI",
        "classes": ["6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "computational thinking", "what is computational thinking", "four pillars", "decomposition",
            "pattern recognition", "abstraction", "algorithm design", "pillars of computational thinking"
        ],
        "badge": "Logic & Code Verified ✓",
        "direct_answer": (
            "Computational Thinking (CT) is a structured problem-solving methodology that breaks down complex "
            "challenges into logical steps that can be automated by humans or computers, founded upon Four Core Pillars: "
            "Decomposition, Pattern Recognition, Abstraction, and Algorithm Design."
        ),
        "steps": [
            ("1. Pillar 1: Decomposition (Breaking Down)",
             "Deconstructing a complex, monolithic problem into smaller, manageable, self-contained sub-problems.\n"
             "• Example: Building an online school portal decomposes into Student Login, Attendance Tracker, Gradebook, and Timetable modules."),
            ("2. Pillar 2: Pattern Recognition (Finding Regularities)",
             "Observing similarities, repetitions, and trends across problems and historical data.\n"
             "• Example: Detecting recurring weather patterns or diagnosing code errors based on past bug signatures."),
            ("3. Pillar 3: Abstraction (Focusing on Essentials)",
             "Filtering out irrelevant, superfluous background details to focus exclusively on necessary core variables.\n"
             "• Example: A metro rail map simplifies geography into straight colored lines and station dots, omitting buildings and road contours."),
            ("4. Pillar 4: Algorithm Design (Step-by-Step Solution)",
             "Formulating an ordered, finite, unambiguous sequence of instructions to solve the problem or achieve an output.\n"
             "• Example: Standard recipe instructions, long division steps, or a sorting algorithm script."),
            ("5. Curriculum Verification",
             "Verified against CBSE Class 6–8 Computational Thinking & AI Curriculum guidelines. (Logic & Code Verified ✓)")
        ]
    },
    {
        "id": "ai_project_cycle",
        "title": "The AI Project Cycle & 4Ws Problem Canvas",
        "subject": "Computational Thinking & AI",
        "classes": ["6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "ai project cycle", "what is ai project cycle", "4ws canvas", "4ws problem canvas",
            "problem scoping", "data acquisition", "data exploration", "modelling", "model evaluation",
            "confusion matrix", "precision", "recall", "f1 score"
        ],
        "badge": "Logic & Code Verified ✓",
        "direct_answer": (
            "The AI Project Cycle is the 5-stage framework for developing reliable Artificial Intelligence systems: "
            "1. Problem Scoping (4Ws Canvas: Who, What, Where, Why), 2. Data Acquisition, 3. Data Exploration, "
            "4. Modelling (Rule-based vs Learning-based), and 5. Evaluation (Confusion Matrix, Precision, Recall, F1 Score)."
        ),
        "steps": [
            ("1. Stage 1: Problem Scoping & 4Ws Canvas",
             "• Who: Who are the stakeholders affected by the problem?\n"
             "• What: What is the nature of the problem, and what evidence proves its existence?\n"
             "• Where: Where is the operational context or geographical location of the issue?\n"
             "• Why: Why will solving this problem bring tangible value to the stakeholders?"),
            ("2. Stage 2 & 3: Data Acquisition & Exploration",
             "• Data Acquisition: Collecting reliable, authentic data through sensors, surveys, web APIs, or databases.\n"
             "• Data Exploration: Cleaning null values, visualizing distributions via plots, and discovering feature correlations."),
            ("3. Stage 4: Modelling",
             "• Rule-Based AI: Programmer writes deterministic hard-coded if-else logic.\n"
             "• Learning-Based AI (Machine Learning): Model learns patterns and relationships autonomously from training data (Supervised, Unsupervised, Reinforcement Learning)."),
            ("4. Stage 5: Evaluation & Metrics",
             "Evaluates performance on unseen test data using a 2×2 Confusion Matrix:\n"
             "• Accuracy: (TP + TN) / Total Predictions\n"
             "• Precision: TP / (TP + FP) [crucial when False Positives are costly, e.g. spam detection]\n"
             "• Recall: TP / (TP + FN) [crucial when False Negatives are dangerous, e.g. medical diagnosis]\n"
             "• F1 Score: Harmonic mean = 2 × (Precision × Recall) / (Precision + Recall)"),
            ("5. Curriculum Verification",
             "Verified against CBSE Class 9 & 10 AI (Subject Code 417) curriculum. (Logic & Code Verified ✓)")
        ]
    },

    # =========================================================================
    # 4. COMMERCE, ACCOUNTANCY & BUSINESS STUDIES (Classes 11 - 12)
    # =========================================================================
    {
        "id": "accounting_principles",
        "title": "Basic Accounting Principles and Golden Rules",
        "subject": "Accountancy",
        "classes": ["11", "12", "11_Commerce", "12_Commerce"],
        "triggers": [
            "accounting", "what is accounting", "accounting equation", "golden rules of accounting",
            "debit and credit", "accrual principle", "balance sheet", "journal entry", "asset", "liability"
        ],
        "badge": "Curriculum Fact Verified ✓",
        "direct_answer": (
            "Accounting is the systematic process of identifying, measuring, recording, classifying, summarizing, "
            "and communicating financial transactions in terms of money, governed by the Fundamental Accounting Equation: "
            "Assets = Liabilities + Capital (Owner's Equity)."
        ),
        "steps": [
            ("1. The Fundamental Accounting Equation",
             "Assets = Liabilities + Capital\n"
             "• Assets: Economic resources owned by the enterprise (Cash, Bank, Debtors, Stock, Machinery, Building).\n"
             "• Liabilities: Obligations or debts owed to outsiders (Creditors, Bank Overdraft, Loans).\n"
             "• Capital: Net financial stake contributed by the owner (Capital = Assets - Liabilities)."),
            ("2. The Three Traditional Golden Rules of Accounting",
             "1. Real Accounts (Tangible/Intangible Assets): Debit what comes in, Credit what goes out.\n"
             "2. Personal Accounts (Persons, Firms, Companies): Debit the receiver, Credit the giver.\n"
             "3. Nominal Accounts (Expenses, Incomes, Gains, Losses): Debit all expenses & losses, Credit all incomes & gains."),
            ("3. Modern Approach of Account Classification (CLEAR)",
             "• Capital: Increases on Credit, Decreases on Debit\n"
             "• Liabilities: Increases on Credit, Decreases on Debit\n"
             "• Expenses: Increases on Debit, Decreases on Credit\n"
             "• Assets: Increases on Debit, Decreases on Credit\n"
             "• Revenue/Income: Increases on Credit, Decreases on Debit"),
            ("4. Vital Accounting Principles",
             "• Accrual Principle: Revenue and expenses are recognized when earned or incurred, regardless of cash receipt or payment.\n"
             "• Dual Aspect Concept: Every transaction has a two-fold debit and credit impact.\n"
             "• Business Entity Concept: The business is treated as a separate distinct legal entity from its owners."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 11 Accountancy Chapter 2: 'Theory Base of Accounting'. (Curriculum Fact Verified ✓)")
        ]
    },
    {
        "id": "fayol_management",
        "title": "Henri Fayol's 14 Principles of Management",
        "subject": "Business Studies",
        "classes": ["12", "12_Commerce"],
        "triggers": [
            "fayol", "henri fayol", "principles of management", "14 principles", "taylor vs fayol",
            "unity of command", "unity of direction", "scalar chain", "espirit de corps", "division of work"
        ],
        "badge": "Curriculum Fact Verified ✓",
        "direct_answer": (
            "French industrialist Henri Fayol formulated the 14 Classical Principles of Administrative Management, "
            "providing a universal operational guide for managers to coordinate organizational resources efficiently."
        ),
        "steps": [
            ("1. Division of Work & Authority",
             "1. Division of Work: Specialization of labor leads to increased efficiency and accuracy.\n"
             "2. Authority and Responsibility: Authority is the right to give orders; it must always be balanced with commensurate responsibility.\n"
             "3. Discipline: Adherence to organizational rules, respect for agreements, and judicious application of penalties."),
            ("2. Command, Direction & Subordination",
             "4. Unity of Command: An employee should receive instructions from only ONE superior to avoid confusion and dual orders.\n"
             "5. Unity of Direction: One head and one plan for a group of activities having the same objective.\n"
             "6. Subordination of Individual Interest to General Interest: The organization's overarching goals supersede individual interests.\n"
             "7. Remuneration: Fair, competitive compensation providing reasonable satisfaction to employees and employers."),
            ("3. Hierarchy & Order",
             "8. Centralization and Decentralization: Balancing top-level strategic control with delegated operational autonomy.\n"
             "9. Scalar Chain: Formal line of authority from top to bottom. (Fayol permitted 'Gang Plank' for direct horizontal emergency communication).\n"
             "10. Order: 'A place for everything/everyone, and everything/everyone in its place'.\n"
             "11. Equity: Kindliness and justice in dealing with subordinates."),
            ("4. Tenure, Initiative & Teamwork",
             "12. Stability of Tenure of Personnel: Minimizing employee turnover to foster institutional knowledge.\n"
             "13. Initiative: Encouraging staff to conceive and execute innovative plans.\n"
             "14. Esprit de Corps: Promoting team harmony and mutual trust ('Union is Strength')."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 12 Business Studies Chapter 2: 'Principles of Management'. (Curriculum Fact Verified ✓)")
        ]
    },

    # =========================================================================
    # 5. LANGUAGES (English, Hindi, Sanskrit)
    # =========================================================================
    {
        "id": "english_parts_of_speech",
        "title": "English Grammar: Eight Parts of Speech",
        "subject": "English",
        "classes": ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "Foundation"],
        "triggers": [
            "parts of speech", "noun", "pronoun", "verb", "adjective", "adverb", "preposition",
            "conjunction", "interjection", "what is noun", "what is verb", "what is adjective"
        ],
        "badge": "Language Rule Verified ✓",
        "direct_answer": (
            "In English grammar, words are categorized into Eight Parts of Speech based on their syntactic "
            "function in a sentence: Noun, Pronoun, Verb, Adjective, Adverb, Preposition, Conjunction, and Interjection."
        ),
        "steps": [
            ("1. Noun & Pronoun",
             "• Noun: The naming word for a person, place, animal, thing, or abstract idea (e.g. Ramesh, Delhi, tiger, honesty, courage).\n"
             "• Pronoun: A word used in place of a noun to avoid monotonous repetition (e.g. he, she, it, they, someone, who)."),
            ("2. Verb, Adjective & Adverb",
             "• Verb: An action, state of being, or occurrence word (e.g. run, write, is, become, accelerated).\n"
             "• Adjective: A modifier that describes or qualifies a noun/pronoun (e.g. brave, ancient, green, circular, intelligent).\n"
             "• Adverb: A modifier that describes a verb, adjective, or another adverb, indicating manner, time, place, or degree (e.g. quickly, yesterday, everywhere, very)."),
            ("3. Preposition, Conjunction & Interjection",
             "• Preposition: Indicates spatial, temporal, or logical relationship between a noun and other words (e.g. on, in, through, between, during).\n"
             "• Conjunction: Connects words, phrases, or clauses (e.g. and, but, because, although, since).\n"
             "• Interjection: An exclamatory word expressing sudden emotion (e.g. Hurrah!, Alas!, Wow!, Ouch!)."),
            ("4. Illustrative Sentence Analysis",
             "'The brave girl ran quickly across the road because it was raining.'\n"
             "• Girl/road: Nouns | brave: Adjective | ran: Verb | quickly: Adverb | across: Preposition | because: Conjunction | it: Pronoun."),
            ("5. Curriculum Verification",
             "Verified against NCERT English Grammar syllabus across Classes 5 to 10. (Language Rule Verified ✓)")
        ]
    },
    {
        "id": "hindi_grammar_sangya",
        "title": "हिंदी व्याकरण: संज्ञा एवं उसके भेद",
        "subject": "Hindi",
        "classes": ["3", "4", "5", "6", "7", "8", "9", "10", "Foundation"],
        "triggers": [
            "संज्ञा", "संज्ञा की परिभाषा", "संज्ञा किसे कहते हैं", "संज्ञा के भेद", "व्यक्तिवाचक संज्ञा",
            "जातिवाचक संज्ञा", "भाववाचक संज्ञा", "sangya", "what is sangya"
        ],
        "badge": "Language Rule Verified ✓",
        "direct_answer": (
            "किसी व्यक्ति, प्राणी, वस्तु, स्थान अथवा भाव के नाम को 'संज्ञा' कहते हैं। "
            "जैसे: राम (व्यक्ति), गाय (प्राणी), पुस्तक (वस्तु), दिल्ली (स्थान), और सुंदरता/ईमानदारी (भाव)।"
        ),
        "steps": [
            ("1. संज्ञा की मानक परिभाषा",
             "संसार के किसी भी नाम को संज्ञा कहा जाता है। वाक्य में संज्ञा कर्ता, कर्म तथा पूरक के रूप में प्रयुक्त होती है।"),
            ("2. संज्ञा के तीन मुख्य भेद (प्रकार)",
             "1. व्यक्तिवाचक संज्ञा: जो शब्द किसी विशेष व्यक्ति, विशेष स्थान अथवा विशेष वस्तु का बोध कराते हैं। (उदा: हिमालय, गंगा, महात्मा गांधी, भारत, रामायण)।\n"
             "2. जातिवाचक संज्ञा: जो शब्द किसी प्राणी, वस्तु अथवा स्थान की संपूर्ण जाति या वर्ग का बोध कराते हैं। (उदा: नदी, पर्वत, बालक, नगर, पेड़, पुस्तक)।\n"
             "   • इसके अंतर्गत दो उपभेद भी माने जाते हैं: (क) द्रव्यवाचक (सोना, पानी, दूध, तेल), (ख) समूहवाचक (सेना, कक्षा, भीड़, परिवार)।\n"
             "3. भाववाचक संज्ञा: जो शब्द किसी व्यक्ति या वस्तु के गुण, दोष, दशा, अवस्था अथवा मन के भाव का बोध कराते हैं, जिन्हें केवल अनुभव किया जा सकता है (देखा या छुआ नहीं जा सकता)। (उदा: मिठास, बचपन, बुढ़ापा, ईमानदारी, वीरता, मित्रता)।"),
            ("3. भाववाचक संज्ञा निर्माण के नियम",
             "• जातिवाचक संज्ञा से: मित्र ➔ मित्रता, मानव ➔ मानवता, बच्चा ➔ बचपन।\n"
             "• सर्वनाम से: अपना ➔ अपनापन, निज ➔ निजत्व।\n"
             "• विशेषण से: मीठा ➔ मिठास, वीर ➔ वीरता, चतुर ➔ चतुराई।\n"
             "• क्रिया से: लिखना ➔ लिखावट, चढ़ना ➔ चढ़ाई, पढ़ना ➔ पढ़ाई।"),
            ("4. परीक्षा-उपयोगी उदाहरण",
             "'महात्मा गांधी ने देश को अहिंसा का मार्ग दिखाया।'\n"
             "• 'महात्मा गांधी' = व्यक्तिवाचक संज्ञा\n"
             "• 'देश' = जातिवाचक संज्ञा\n"
             "• 'अहिंसा' = भाववाचक संज्ञा"),
            ("5. पाठ्यक्रम सत्यापन",
             "एनसीईआरटी एवं सीबीएसई कक्षा 5 से 10 मानक हिंदी व्याकरण द्वारा सत्यापित। (Language Rule Verified ✓)")
        ]
    },
    {
        "id": "nutrition_and_digestion",
        "title": "Components of Food, Nutrients & Digestion",
        "subject": "Science",
        "classes": ["3", "4", "5", "6", "7", "8", "9", "10", "Foundation"],
        "triggers": [
            "nutrient", "nutrients", "balanced diet", "carbohydrate", "carbohydrates", "protein", "proteins",
            "fats", "vitamins", "minerals", "roughage", "deficiency disease", "scurvy", "rickets", "anemia",
            "beriberi", "goitre", "digestion", "digestive system", "stomach function", "small intestine"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "Nutrients are chemical substances present in food that provide energy, support tissue growth and repair, "
            "and regulate physiological functions. The seven primary dietary components are Carbohydrates, Fats, Proteins, "
            "Vitamins, Minerals, Dietary Fibre (Roughage), and Water."
        ),
        "steps": [
            ("1. Major Nutrient Groups & Their Primary Roles",
             "• Carbohydrates & Fats: Energy-giving foods. Fats provide more than double the energy per gram compared to carbohydrates (e.g. cereals, rice, butter, nuts).\n"
             "• Proteins: Body-building foods required for cell division, tissue repair, enzyme synthesis, and muscle growth (e.g. pulses, eggs, milk, fish).\n"
             "• Vitamins & Minerals: Protective foods that safeguard against pathogens and regulate metabolic reactions (e.g. fresh fruits, green leafy vegetables).\n"
             "• Dietary Fibre (Roughage) & Water: Essential for bowel regularity, preventing constipation, and cellular fluid transport."),
            ("2. Deficiency Diseases and Their Symptoms",
             "• Vitamin A: Night blindness (poor vision in dim light).\n"
             "• Vitamin B1: Beriberi (weak muscles, fatigue).\n"
             "• Vitamin C: Scurvy (bleeding gums, slow wound healing).\n"
             "• Vitamin D / Calcium: Rickets (soft, bent bones) & tooth decay.\n"
             "• Iron: Anemia (low hemoglobin, pale skin, fatigue).\n"
             "• Iodine: Goitre (swollen thyroid gland in neck, mental disability in children)."),
            ("3. The Human Digestive System Pathway",
             "Mouth (salivary amylase digests starch) ➔ Oesophagus (peristaltic waves) ➔ Stomach (gastric juice with HCl and pepsin breaks down proteins) ➔ Small Intestine (bile from liver emulsifies fats; pancreatic enzymes digest proteins, carbs, fats; villi absorb nutrients into bloodstream) ➔ Large Intestine (reabsorbs water) ➔ Rectum & Anus (egestion)."),
            ("4. Balanced Diet Definition",
             "A diet containing all essential nutrient groups, roughage, and water in the appropriate proportions for healthy growth and energy needs."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 6 Science Chapter 2: 'Components of Food' & Class 7 Science: 'Nutrition in Animals'. (Formula & Concept Verified ✓)")
        ]
    },
    {
        "id": "microorganisms_friend_foe",
        "title": "Microorganisms: Classification, Benefits & Pathogens",
        "subject": "Science",
        "classes": ["5", "6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "microorganism", "microorganisms", "microbe", "microbes", "bacteria", "fungi", "protozoa",
            "algae", "virus", "viruses", "lactobacillus", "yeast fermentation", "pasteurisation",
            "antibiotic", "penicillin", "vaccine", "pathogen", "communicable disease"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "Microorganisms (microbes) are microscopic, single-celled or multicellular organisms invisible to the naked eye, "
            "classified into four major biological groups: Bacteria, Fungi, Protozoa, and Algae, alongside Viruses "
            "which reproduce exclusively inside host living cells."
        ),
        "steps": [
            ("1. The Four Primary Groups of Microorganisms",
             "• Bacteria: Unicellular prokaryotes with diverse shapes (bacilli/rod, cocci/spherical, spirilla/spiral). Example: Lactobacillus, Rhizobium, E. coli.\n"
             "• Fungi: Non-green heterotrophic organisms. Example: Bread mold (Rhizopus), Yeast (Saccharomyces), Penicillium, Mushroom.\n"
             "• Protozoa: Unicellular eukaryotic heterotrophs. Example: Amoeba, Paramecium, Plasmodium (malaria parasite).\n"
             "• Algae: Simple autotrophic photosynthetic organisms. Example: Spirogyra, Chlamydomonas."),
            ("2. Viruses (Edge of Life)",
             "Viruses lack cellular machinery and remain dormant outside hosts, but hijack the metabolic apparatus of host plant, animal, or bacterial cells to replicate."),
            ("3. Beneficial Microbes in Daily Life & Medicine",
             "• Food Industry: Lactobacillus bacterium converts lactose into lactic acid, turning milk into curd; Yeast ferments sugars into alcohol and CO₂, causing bread dough to rise.\n"
             "• Agriculture: Rhizobium bacteria in leguminous root nodules fix atmospheric nitrogen into nitrates to enrich soil fertility.\n"
             "• Medicine: Antibiotics (e.g. Penicillin discovered by Alexander Fleming) kill bacterial pathogens; Vaccines (Edward Jenner) introduce weakened microbes to produce antibodies."),
            ("4. Food Preservation Methods",
             "• Pasteurisation (Louis Pasteur): Heating milk to ~70°C for 15–30 seconds and rapidly chilling it to kill pathogenic bacteria.\n"
             "• Preservatives: Salt (osmotic dehydration in pickles), Sugar (jams/jellies), Oil & Vinegar, Chemical preservatives (Sodium benzoate)."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 8 Science Chapter 2: 'Microorganisms: Friend and Foe'. (Formula & Concept Verified ✓)")
        ]
    },
    {
        "id": "light_reflection_and_lenses",
        "title": "Light: Reflection, Refraction, Mirrors and Lenses",
        "subject": "Science",
        "classes": ["6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "reflection of light", "laws of reflection", "refraction", "concave mirror", "convex mirror",
            "concave lens", "convex lens", "focal length", "real vs virtual image", "myopia", "hypermetropia",
            "dispersion of light", "spectrum"
        ],
        "badge": "Formula & Concept Verified ✓",
        "direct_answer": (
            "Light travels in straight lines (rectilinear propagation). When it strikes an interface, it undergoes "
            "Reflection (bouncing back into the same medium) or Refraction (bending due to a change in speed across "
            "different optical media)."
        ),
        "steps": [
            ("1. The Two Laws of Reflection",
             "1. The incident ray, the reflected ray, and the normal to the reflecting surface at the point of incidence all lie in the same plane.\n"
             "2. The angle of incidence equals the angle of reflection: ∠i = ∠r."),
            ("2. Real vs Virtual Images",
             "• Real Image: Formed by the actual convergence of light rays; can be caught on a screen; always inverted.\n"
             "• Virtual Image: Formed when rays appear to diverge from a point behind the surface; cannot be caught on a screen; always erect/upright."),
            ("3. Spherical Mirrors and Lenses",
             "• Concave Mirror: Converging mirror. Used in dentist tools, torches, vehicle headlights, and solar furnaces.\n"
             "• Convex Mirror: Diverging mirror giving a virtual, erect, and diminished image with a wide field of view. Used as vehicle rear-view mirrors.\n"
             "• Convex Lens: Converging lens. Thicker in the middle than edges; used in magnifying glasses, microscopes, and to correct Hypermetropia (far-sightedness).\n"
             "• Concave Lens: Diverging lens. Thinner in the middle; produces virtual, upright, diminished images; used to correct Myopia (short-sightedness)."),
            ("4. Refraction and Snell's Law",
             "Refraction occurs because light travels at different velocities in different optical densities (n = c / v). Snell's Law: sin i / sin r = constant (refractive index n₂₁)."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 7 Science Chapter 15 & Class 10 Science Chapter 10: 'Light - Reflection and Refraction'. (Formula & Concept Verified ✓)")
        ]
    },
    {
        "id": "dandi_march_satyagraha",
        "title": "The Dandi March & The Indian National Movement",
        "subject": "Social Science (SST)",
        "classes": ["5", "6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "dandi march", "salt march", "salt satyagraha", "civil disobedience movement",
            "non cooperation movement", "quit india movement", "mahatma gandhi", "sabarmati ashram",
            "1930", "salt tax"
        ],
        "badge": "Curriculum Fact Verified ✓",
        "direct_answer": (
            "The Dandi March (Salt Satyagraha) was a landmark 240-mile civil disobedience protest led by Mahatma Gandhi "
            "from 12 March to 6 April 1930, marching from Sabarmati Ashram to the coastal village of Dandi (Gujarat) "
            "to defy the British colonial salt monopoly by manufacturing salt from seawater."
        ),
        "steps": [
            ("1. Historical Context & Strategic Symbolism",
             "Salt was a universal daily necessity consumed equally by the rich and poor. The British colonial salt monopoly and oppressive salt tax were seen as an unjust imposition on basic human survival, making salt the ideal unifying symbol of resistance across all castes, religions, and economic classes."),
            ("2. The March Route and Key Dates",
             "• Start Date: 12 March 1930 from Sabarmati Ashram, Ahmedabad, with 78 chosen satyagrahis.\n"
             "• Journey: 240 miles (385 km) covered on foot over 24 days through rural Gujarat, drawing tens of thousands of supportive villagers.\n"
             "• Culmination: 6 April 1930 at Dandi beach, where Gandhi picked up a lump of natural sea salt, breaking the British salt law and launching the nationwide Civil Disobedience Movement."),
            ("3. Nationwide Impact & Mass Participation",
             "• Millions across India boycotted foreign cloth, picketed liquor shops, and refused to pay land revenue/chaukidari taxes.\n"
             "• Massive participation of Indian women, led by leaders such as Sarojini Naidu, marked a turning point in gender mobilization.\n"
             "• Over 60,000 freedom fighters, including Mahatma Gandhi and Jawaharlal Nehru, were arrested by colonial authorities."),
            ("4. Significance in the Freedom Struggle",
             "The Salt March brought the Indian independence movement to the forefront of global attention, forced the British government to negotiate on equal terms during the 1931 Gandhi-Irwin Pact, and demonstrated the potent moral power of non-violent Satyagraha."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 5 EVS Chapter 6 & NCERT Class 10 History Chapter 2: 'Nationalism in India'. (Curriculum Fact Verified ✓)")
        ]
    },
    {
        "id": "monsoons_and_geography",
        "title": "Climate, Monsoons and Soils of India",
        "subject": "Social Science (SST)",
        "classes": ["5", "6", "7", "8", "9", "10", "11", "12"],
        "triggers": [
            "monsoon", "what is monsoon", "climate of india", "southwest monsoon", "northeast monsoon",
            "tropic of cancer", "soils of india", "alluvial soil", "black soil", "regur soil", "western ghats"
        ],
        "badge": "Curriculum Fact Verified ✓",
        "direct_answer": (
            "The climate of India is described as a 'Monsoon' type, characterized by seasonal reversal of wind direction "
            "driven by differential heating of the landmass and surrounding oceans, primarily bringing rainfall via the "
            "Southwest Monsoon (June to September)."
        ),
        "steps": [
            ("1. Mechanism of the Southwest Monsoon",
             "During summer, intense solar heating over the Indian subcontinent and Tibetan plateau creates a strong low-pressure trough, drawing moisture-laden winds from the high-pressure southern Indian Ocean. As these winds cross the equator, they deflect rightward (Coriolis Effect) and split into two rain-bearing branches:\n"
             "1. Arabian Sea Branch: Strikes the Western Ghats, causing heavy orographic rainfall on coastal windward slopes before advancing over central and northern India.\n"
             "2. Bay of Bengal Branch: Strikes the hills of Northeast India (Cherrapunji/Mawsynram: wettest place on Earth) and deflects along the Himalayas toward the Indo-Gangetic Plains."),
            ("2. Retreating / Northeast Monsoon",
             "During October–November, solar heating shifts southward; winds reverse and blow from northeast to southwest, bringing winter precipitation to the Coromandel coast (Tamil Nadu)."),
            ("3. Major Soil Types of India",
             "• Alluvial Soil: Deposited by Indus, Ganga, and Brahmaputra river systems; exceptionally fertile, rich in potash and phosphoric acid, ideal for wheat, paddy, and sugarcane.\n"
             "• Black / Regur Soil: Formed from weathered volcanic Deccan basalt; clayey, holds moisture, ideal for cotton cultivation.\n"
             "• Red and Yellow Soil: Formed on crystalline igneous rocks under low rainfall; reddish due to iron diffusion.\n"
             "• Laterite Soil: Formed under high temperature and intense monsoon leaching; acidic, utilized for tea, coffee, and cashew crops."),
            ("4. Crucial Importance to the Indian Economy",
             "Over 50% of India's agricultural workforce depends on timely monsoon rains to irrigate Kharif crops (paddy, maize, pulses), heavily impacting food security and annual GDP."),
            ("5. Curriculum Verification",
             "Verified against NCERT Class 9 & 10 Geography: 'Climate' and 'Resources and Development'. (Curriculum Fact Verified ✓)")
        ]
    }
]


def find_matching_concept(query: str, subject_hint: str = "", chapter_hint: str = "") -> Optional[Dict[str, Any]]:
    """Matches a student query against authentic curriculum concepts.
    Returns the concept dictionary if found, else None.
    """
    q_low = query.strip().lower()
    # Normalize punctuation and extra spaces
    clean_q = " ".join("".join(c if c.isalnum() or c.isspace() else " " for c in q_low).split())
    
    sub_hint_low = (subject_hint or "").lower()
    chap_hint_low = (chapter_hint or "").lower()

    # Exact trigger check first
    for c in CURRICULUM_CONCEPTS:
        c_sub_low = c["subject"].lower()
        sub_matches = (
            not sub_hint_low or
            sub_hint_low in c_sub_low or
            c_sub_low in sub_hint_low or
            ("science" in sub_hint_low and "science" in c_sub_low) or
            ("evs" in sub_hint_low and "science" in c_sub_low)
        )
        
        for tr in c["triggers"]:
            tr_clean = " ".join("".join(ch if ch.isalnum() or ch.isspace() else " " for ch in tr.lower()).split())
            if (
                clean_q == tr_clean or
                clean_q.startswith(tr_clean + " ") or
                clean_q.endswith(" " + tr_clean) or
                f" {tr_clean} " in f" {clean_q} " or
                f"what is {tr_clean}" in clean_q or
                f"what are {tr_clean}" in clean_q or
                f"define {tr_clean}" in clean_q or
                f"explain {tr_clean}" in clean_q
            ):
                return c

    # Contextual check if chapter matches concept theme
    if chap_hint_low:
        for c in CURRICULUM_CONCEPTS:
            if c["id"] == "seeds_and_germination" and "seed" in chap_hint_low:
                # If query contains any seed keywords
                if any(w in clean_q for w in ["seed", "seeds", "coat", "cotyledon", "embryo", "germination", "dispers", "disperse"]):
                    return c
            elif c["id"] == "photosynthesis" and ("photo" in chap_hint_low or "plant" in chap_hint_low):
                if any(w in clean_q for w in ["photo", "chlorophyll", "stomata", "make food", "sunlight"]):
                    return c
            elif c["id"] == "water_cycle" and ("water" in chap_hint_low or "rain" in chap_hint_low):
                if any(w in clean_q for w in ["cycle", "evaporat", "condens", "precipitat", "cloud"]):
                    return c
            elif c["id"] == "friction" and "friction" in chap_hint_low:
                if "friction" in clean_q:
                    return c

    return None
