# Authentic CBSE & ICSE Curriculum Question Bank
# Covers Mathematics, Science, Social Science (SST), English, Hindi, Sanskrit, French & Senior Subjects

SUBJECT_QUESTIONS = {
    "Mathematics": [
        ("What is the value of 15 × 8 + 45?", ["165", "155", "175", "145"], 0, "15 × 8 = 120; adding 45 gives 165.", "Easy"),
        ("Which of the following is a prime number?", ["49", "51", "53", "55"], 2, "53 has only two factors: 1 and itself, making it a prime number.", "Easy"),
        ("What is the sum of angles in a quadrilateral?", ["180°", "270°", "360°", "540°"], 2, "The sum of the interior angles of any convex quadrilateral is always 360°.", "Easy"),
        ("Solve for x in: 3x - 7 = 14.", ["5", "7", "6", "8"], 1, "Adding 7 to both sides gives 3x = 21, hence x = 21/3 = 7.", "Easy"),
        ("What is the area of a circle with radius 7 cm? (Take π = 22/7)", ["154 cm²", "44 cm²", "144 cm²", "168 cm²"], 0, "Area = πr² = (22/7) × 7 × 7 = 154 cm².", "Medium"),
        ("What are the roots of the quadratic equation x² - 5x + 6 = 0?", ["2 and 3", "-2 and -3", "1 and 6", "-1 and 6"], 0, "Factorising: (x - 2)(x - 3) = 0 gives roots x = 2 and x = 3.", "Medium"),
        ("In an Arithmetic Progression, if a = 5 and d = 3, what is the 10th term?", ["32", "35", "29", "30"], 0, "an = a + (n - 1)d = 5 + (10 - 1) × 3 = 5 + 27 = 32.", "Medium"),
        ("If sin θ = 3/5, what is the value of cos θ for an acute angle θ?", ["4/5", "3/4", "5/4", "1/2"], 0, "Using cos²θ = 1 - sin²θ = 1 - 9/25 = 16/25, cos θ = 4/5.", "Medium")
    ],
    "Science": [
        ("Which green pigment in plants is essential for photosynthesis?", ["Chlorophyll", "Hemoglobin", "Carotene", "Anthocyanin"], 0, "Chlorophyll inside chloroplasts captures light energy from the sun for photosynthesis.", "Easy"),
        ("What is the powerhouse of the cell?", ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"], 1, "Mitochondria generate most of the chemical energy needed by the cell (ATP).", "Easy"),
        ("What is the chemical formula of common table salt?", ["NaCl", "KCl", "NaOH", "HCl"], 0, "Sodium chloride (NaCl) is known as table salt.", "Easy"),
        ("Which gas turns lime water milky due to the formation of calcium carbonate?", ["Carbon Dioxide (CO₂)", "Oxygen (O₂)", "Hydrogen (H₂)", "Nitrogen (N₂)"], 0, "CO₂ reacts with lime water (Ca(OH)₂) to form insoluble calcium carbonate (CaCO₃).", "Easy"),
        ("What is the SI unit of force?", ["Joule", "Pascal", "Newton", "Watt"], 2, "Force is measured in Newtons (N) in the International System of Units.", "Easy"),
        ("Which law states that current is directly proportional to voltage at constant temperature?", ["Ohm's Law", "Faraday's Law", "Coulomb's Law", "Newton's Law"], 0, "Ohm's Law states that V = IR where R is resistance.", "Medium"),
        ("What type of lens is used to correct myopia (short-sightedness)?", ["Concave lens", "Convex lens", "Bifocal lens", "Cylindrical lens"], 0, "A diverging (concave) lens assists the eye by shifting the focused image onto the retina.", "Medium"),
        ("What is the pH of a neutral aqueous solution at 25°C?", ["0", "7", "14", "1"], 1, "A neutral solution has [H⁺] = [OH⁻] = 10⁻⁷ M, yielding a pH of 7.", "Easy")
    ],
    "Environmental Studies (EVS)": [
        ("Which animal has such acute hearing that it can move its ears in different directions to catch sounds?", ["Tiger", "Frog", "Lizard", "Fish"], 0, "A tiger's ears can rotate in different directions to locate prey sounds.", "Easy"),
        ("What is the main function of chlorophyll in plant leaves?", ["Trapping solar energy for photosynthesis", "Absorbing water from soil", "Repelling insects", "Storing mineral salts"], 0, "Chlorophyll captures sunlight required for synthesizing glucose and oxygen.", "Easy"),
        ("Why does an iron bowl float on water while a small iron nail sinks?", ["Buoyancy and water displacement (Archimedes' principle)", "The nail is heavier than the bowl", "The bowl is magnetic", "Iron dissolves in water"], 0, "The bowl's shape displaces enough water so that the buoyant force balances its weight.", "Medium"),
        ("Which mosquito spreads malaria when it bites humans?", ["Female Anopheles", "Male Anopheles", "Aedes aegypti", "Housefly"], 0, "Female Anopheles mosquitoes carry the microscopic Plasmodium parasite.", "Easy"),
        ("What traditional underground water harvesting tank is built in dry regions of Rajasthan?", ["Tanka", "Borewell", "Canal", "River"], 0, "A Tanka collects rainwater falling on sloping rooftops through PVC pipes.", "Easy"),
        ("Which famous mountain climber became the first Indian woman to reach Mount Everest in 1984?", ["Bachendri Pal", "Kalpana Chawla", "Sunita Williams", "Santosh Yadav"], 0, "Bachendri Pal reached the summit of Mount Everest on May 23, 1984.", "Easy")
    ],
    "Social Science (SST)": [
        ("Who is recognized as the chief architect and Father of the Indian Constitution?", ["Dr. B.R. Ambedkar", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Vallabhbhai Patel"], 0, "Dr. B.R. Ambedkar was the Chairman of the Drafting Committee of the Constituent Assembly.", "Easy"),
        ("In which year did the Dandi March (Salt Satyagraha) led by Mahatma Gandhi take place?", ["1930", "1920", "1942", "1919"], 0, "Mahatma Gandhi launched the Civil Disobedience Movement with the historic 1930 Salt March.", "Easy"),
        ("Which line of latitude divides India almost into two equal halves?", ["Tropic of Cancer (23°30' N)", "Equator (0°)", "Tropic of Capricorn (23°30' S)", "Prime Meridian"], 0, "The Tropic of Cancer passes through 8 Indian states, dividing the country into subtropical and tropical zones.", "Easy"),
        ("What is the minimum voting age for Indian citizens under Universal Adult Franchise?", ["18 years", "21 years", "16 years", "25 years"], 0, "The 61st Constitutional Amendment Act reduced the voting age from 21 to 18 years.", "Easy"),
        ("Which sector of the economy includes agriculture, forestry, and fishing?", ["Primary sector", "Secondary sector", "Tertiary sector", "Quaternary sector"], 0, "The primary sector involves extraction and harvesting of natural resources.", "Easy"),
        ("Which river is known as the 'Dakshin Ganga'?", ["Godavari", "Krishna", "Cauvery", "Narmada"], 0, "The Godavari is the largest river system of Peninsular India, often called Dakshin Ganga.", "Medium"),
        ("What form of government exists when power is shared between central and state governments?", ["Federalism", "Unitary system", "Monarchy", "Oligarchy"], 0, "Federalism divides legislative and administrative powers between levels of government.", "Medium")
    ],
    "English": [
        ("Identify the adverb in the sentence: 'The student solved the problem quickly.'", ["solved", "quickly", "problem", "student"], 1, "'Quickly' modifies the verb 'solved', indicating manner.", "Easy"),
        ("Choose the correct passive voice: 'She wrote a beautiful poem.'", ["A beautiful poem was written by her.", "A beautiful poem is written by her.", "A beautiful poem had written by her.", "A beautiful poem was being written."], 0, "Simple past active 'wrote' transforms to 'was written' in passive voice.", "Medium"),
        ("Which figure of speech is used in: 'The stars danced playfully in the moonlit sky'?", ["Personification", "Simile", "Metaphor", "Hyperbole"], 0, "Attributing human actions (dancing) to non-human entities (stars) is personification.", "Medium"),
        ("What is the antonym of the word 'ANCIENT'?", ["Modern", "Historic", "Antique", "Elderly"], 0, "'Modern' represents contemporary times, the opposite of ancient.", "Easy"),
        ("Complete the sentence with the appropriate preposition: 'He has been studying ___ morning.'", ["since", "for", "from", "at"], 0, "'Since' is used with a specific point of time in the past.", "Easy")
    ],
    "Hindi": [
        ("'कक्कू' कविता के रचयिता कौन हैं और 'कक्कू' का शाब्दिक अर्थ क्या है?", ["रमेशचंद्र शाह (कोयल)", "केदारनाथ अग्रवाल (कौआ)", "सुभद्रा कुमारी चौहान (तोता)", "प्रेमचंद (बुलबुल)"], 0, "कक्कू कविता में कवि रमेशचंद्र शाह ने कक्कू नाम के लड़के का वर्णन किया है, जिसका शाब्दिक अर्थ कोयल होता है।", "Easy"),
        ("किसी व्यक्ति, वस्तु, स्थान या भाव के नाम को क्या कहते हैं?", ["संज्ञा", "सर्वनाम", "विशेषण", "क्रिया"], 0, "किसी व्यक्ति, प्राणी, वस्तु, स्थान अथवा भाव के नाम को संज्ञा कहा जाता है।", "Easy"),
        ("'सूर्योदय' शब्द का सही संधि विच्छेद क्या होगा?", ["सूर्य + उदय (गुण स्वर संधि)", "सूर्य + दय", "सूर्यो + दय", "सूर्या + उदय"], 0, "सूर्य + उदय मिलकर 'सूर्योदय' बनता है, जो गुण स्वर संधि का उदाहरण है (अ + उ = ओ)।", "Medium"),
        ("'आँखों का तारा होना' मुहावरे का सही अर्थ क्या है?", ["बहुत प्यारा होना", "कम दिखाई देना", "गुस्सा होना", "धोखा देना"], 0, "'आँखों का तारा होना' का अर्थ है अत्यधिक प्रिय अथवा प्यारा होना।", "Easy"),
        ("रचना के आधार पर 'वह परिश्रमी है इसलिए सफल हुआ' कैसा वाक्य है?", ["संयुक्त वाक्य", "सरल वाक्य", "मिश्र वाक्य", "प्रश्नवाचक वाक्य"], 0, "'इसलिए' संयोजक द्वारा दो स्वतंत्र उपवाक्यों को जोड़ने के कारण यह संयुक्त वाक्य है।", "Medium")
    ],
    "Sanskrit": [
        ("'पठति' रूप किस लकार एवं पुरुष का है?", ["लट् लकार, प्रथम पुरुष, एकवचन", "लृट् लकार, मध्यम पुरुष", "लङ् लकार, उत्तम पुरुष", "लोट् लकार, प्रथम पुरुष"], 0, "'पठति' लट् लकार (वर्तमान काल) प्रथम पुरुष एकवचन का रूप है।", "Easy"),
        ("'बालकः कन्दुकेन क्रीडति' — इस वाक्य में कौन सी विभक्ति का प्रयोग साधन के अर्थ में हुआ है?", ["तृतीया विभक्ति (करण कारक)", "प्रथमा विभक्ति", "द्वितीया विभक्ति", "पञ्चमी विभक्ति"], 0, "क्रिया के साधन (कन्दुक / गेंद) में करण कारक के नियम से तृतीया विभक्ति प्रयुक्त होती है।", "Easy"),
        ("'विद्या ददाति विनयं' — इस प्रसिद्ध सूक्ति का क्या अर्थ है?", ["विद्या विनम्रता प्रदान करती है", "विद्या धन देती है", "विद्या बल देती है", "विद्या घमंड देती है"], 0, "संस्कृत सूक्ति के अनुसार सच्ची विद्या मनुष्य को विनम्र और शीलवान बनाती है।", "Easy"),
        ("'गच्छति' धातु रूप का मूल धातु क्या है?", ["गम् (जाना)", "खाद्", "दृश्", "पठ्"], 0, "'गच्छति' रूप 'गम्' धातु का लट् लकार प्रथम पुरुष एकवचन है।", "Medium")
    ],
    "French": [
        ("Comment dit-on 'Good morning' ou 'Hello' en français?", ["Bonjour", "Bonsoir", "Bonne nuit", "Au revoir"], 0, "'Bonjour' is the standard polite French greeting during the daytime.", "Easy"),
        ("Quel est l'article défini masculin singulier en français?", ["Le", "La", "Les", "Une"], 0, "'Le' is the masculine singular definite article (e.g. le tableau, le livre).", "Easy"),
        ("Conjuguez le verbe 'Être' (to be) avec le pronom 'Nous':", ["Nous sommes", "Nous êtes", "Nous avons", "Nous vont"], 0, "The present indicative conjugation of 'être' with 'nous' is 'nous sommes'.", "Easy"),
        ("Que signifie l'expression 'Comment vous appelez-vous?' en anglais?", ["What is your name?", "How old are you?", "Where do you live?", "How are you doing?"], 0, "'Comment vous appelez-vous?' translates to 'What is your name?' (formal).", "Easy"),
        ("Quel auxiliaire utilise-t-on au passé composé pour le verbe 'Aller'?", ["Être (ex: Je suis allé)", "Avoir", "Faire", "Venir"], 0, "Verbs of movement like 'aller' use the auxiliary 'être' in passé composé.", "Medium")
    ],
    "Physics": [
        ("What is the acceleration due to gravity (g) near the surface of Earth?", ["9.8 m/s²", "10.8 m/s²", "8.9 m/s²", "9.8 km/s²"], 0, "Standard acceleration due to Earth's gravity is approximately 9.8 m/s².", "Easy"),
        ("Which of the following is a scalar quantity?", ["Work", "Force", "Velocity", "Acceleration"], 0, "Work (W = F · d) is the dot product of two vectors and has magnitude only, making it a scalar.", "Medium"),
        ("What happens to the resistance of a metallic conductor when temperature increases?", ["It increases", "It decreases", "Remains constant", "Becomes zero"], 0, "Thermal vibrations increase electron scattering in metals, raising electrical resistance.", "Medium")
    ],
    "Chemistry": [
        ("What is the oxidation state of Manganese in KMnO₄?", ["+7", "+6", "+4", "+2"], 0, "K (+1) + Mn (x) + 4(-2) = 0 => x - 7 = 0 => x = +7.", "Medium"),
        ("Which gas is liberated when an active metal reacts with dilute acid?", ["Hydrogen (H₂)", "Oxygen (O₂)", "Carbon Dioxide", "Nitrogen"], 0, "Active metals displace hydrogen from acids: Zn + 2HCl → ZnCl₂ + H₂↑.", "Easy"),
        ("Which quantum number determines the shape of an atomic orbital?", ["Azimuthal quantum number (l)", "Principal (n)", "Magnetic (m)", "Spin (s)"], 0, "The azimuthal (orbital angular momentum) quantum number l defines s, p, d, f shapes.", "Medium")
    ],
    "Biology": [
        ("What is the site of aerobic cellular respiration in eukaryotic cells?", ["Mitochondria", "Ribosomes", "Golgi apparatus", "Lysosomes"], 0, "The Krebs cycle and oxidative phosphorylation take place inside the mitochondria.", "Easy"),
        ("Which blood group is known as the universal donor in human blood groups?", ["O negative (O-)", "AB positive", "A positive", "B negative"], 0, "Type O negative lacks A, B, and Rh antigens, avoiding recipient immune reactions.", "Easy")
    ],
    "Accountancy": [
        ("Which accounting principle states that revenue is recognized when earned, regardless of cash receipt?", ["Accrual Principle", "Cash Basis", "Conservatism", "Matching Principle"], 0, "Under accrual accounting, transactions are recorded when economic value is transferred.", "Easy"),
        ("What is the primary formula for the basic accounting equation?", ["Assets = Liabilities + Owner's Equity", "Assets = Liabilities - Equity", "Liabilities = Assets + Equity", "Profit = Revenue + Expenses"], 0, "The fundamental double-entry balance equation is Assets = Liabilities + Capital.", "Easy")
    ],
    "Business Studies": [
        ("Who formulated the 14 Principles of Management?", ["Henri Fayol", "F.W. Taylor", "Peter Drucker", "Elton Mayo"], 0, "French engineer Henri Fayol authored the 14 Classical Principles of Administrative Management.", "Easy"),
        ("What are the 4 Ps of the traditional Marketing Mix?", ["Product, Price, Place, Promotion", "People, Process, Product, Promotion", "Plan, Price, Position, Promotion", "Packaging, Price, Placement, Profit"], 0, "The foundational marketing framework consists of Product, Price, Place, and Promotion.", "Easy")
    ],
    "Economics": [
        ("What does Gross Domestic Product (GDP) measure?", ["Total monetary value of final goods & services produced in a country in a year", "Total exports of a nation", "Total revenue collected by government", "Average household income"], 0, "GDP is the market value of all officially recognized final goods and services produced within a nation over a specified period.", "Easy"),
        ("Which institution functions as the Central Bank of India?", ["Reserve Bank of India (RBI)", "State Bank of India (SBI)", "SEBI", "NITI Aayog"], 0, "The RBI regulates monetary policy, currency issuance, and the commercial banking sector in India.", "Easy")
    ],
    "Artificial Intelligence": [
        ("What are the three core domains of Artificial Intelligence?", ["Data Science, Computer Vision, and Natural Language Processing", "Hardware, Software, and Firmware", "Python, Java, and C++", "Robotics, Automation, and Electronics"], 0, "AI applications are classified into three primary technical domains: Data Science, Computer Vision (CV), and Natural Language Processing (NLP).", "Easy"),
        ("In the AI Project Cycle, what does the '4Ws Canvas' help establish?", ["Problem Scoping (Who, What, Where, Why)", "Data Acquisition", "Model Evaluation", "Neural Network Architecture"], 0, "The 4Ws Problem Canvas identifies Who is affected, What the issue is, Where it happens, and Why solving it matters.", "Easy"),
        ("Which metric is defined as True Positives divided by total predicted positives (TP / (TP + FP))?", ["Precision", "Recall", "Accuracy", "F1 Score"], 0, "Precision measures the proportion of positive identifications that were actually correct: TP / (TP + FP).", "Medium"),
        ("What is the primary purpose of a Confusion Matrix in AI evaluation?", ["To tabulate True Positives, True Negatives, False Positives, and False Negatives", "To confuse the classifier", "To normalize text data", "To increase GPU clock speed"], 0, "A Confusion Matrix is a 2x2 grid representing prediction outcomes vs actual ground truth.", "Easy"),
        ("Which algorithm represents text as word frequencies irrespective of grammar or word order?", ["Bag of Words (BoW)", "Linear Regression", "Convolutional Filter", "K-Means"], 0, "The Bag of Words model counts word occurrences across documents while disregarding sequence.", "Medium")
    ],
    "Computational Thinking & AI": [
        ("Which pillar of Computational Thinking involves breaking down a complex problem into smaller parts?", ["Decomposition", "Pattern Recognition", "Abstraction", "Algorithm Design"], 0, "Decomposition reduces complexity by dividing a system or task into manageable sub-components.", "Easy"),
        ("What is 'Abstraction' in computational problem solving?", ["Filtering out irrelevant details to focus on vital concepts", "Writing code in binary", "Connecting hardware cables", "Repeating loops indefinitely"], 0, "Abstraction captures the essential characteristics of an entity while hiding unnecessary implementation details.", "Easy"),
        ("What is an Algorithm?", ["A step-by-step verifiable procedure for solving a specific problem", "A type of computer screen", "A storage device", "An internet protocol"], 0, "An algorithm is an unambiguous, finite sequence of rigorous instructions.", "Easy"),
        ("In flowcharts, which geometric shape represents a decision/conditional test?", ["Diamond", "Rectangle", "Oval", "Parallelogram"], 0, "A diamond symbol specifies a decision branching condition (e.g. Yes/No, True/False).", "Easy")
    ],
    "Data Science": [
        ("Which Python library is the standard foundation for data manipulation and tabular DataFrames?", ["Pandas", "PyGame", "Django", "Flask"], 0, "Pandas provides high-performance data structures like Series and DataFrames for data analysis.", "Easy"),
        ("What does a Z-score of +2.0 indicate about a data point?", ["It is 2 standard deviations above the population mean", "It is twice the median", "It is an invalid error", "It is 2% of the sample"], 0, "The Z-score z = (x - μ) / σ measures the distance from the mean in standard deviation units.", "Medium"),
        ("Which type of machine learning is primarily used to predict continuous numerical values (e.g., house prices)?", ["Regression (Supervised Learning)", "Classification", "Clustering", "Reinforcement Learning"], 0, "Linear regression models continuous target variables based on input predictors.", "Easy")
    ],
    "Robotics and Artificial Intelligence": [
        ("Which sensor measures distance by emitting high-frequency sound waves and calculating time-of-flight?", ["Ultrasonic Sensor (HC-SR04)", "Infrared (IR) Sensor", "LDR (Light Dependent Resistor)", "Piezoelectric Buzzer"], 0, "Ultrasonic sensors use the velocity of sound in air (343 m/s) to calculate Distance = (Time × Speed) / 2.", "Easy"),
        ("What type of motor allows precise control of angular position (typically 0° to 180°) via PWM signals?", ["Servo Motor", "DC Brushless Motor", "Stepper Motor", "AC Induction Motor"], 0, "Servo motors contain closed-loop positional feedback circuitry controlled by pulse-width modulation.", "Easy"),
        ("What is the function of the L298N H-Bridge module in robot design?", ["Bi-directional speed and direction control of DC motors", "Wireless internet communication", "Audio processing", "Optical image capture"], 0, "An H-bridge circuit enables independent forward/reverse current polarity switching for motor drives.", "Medium")
    ],
    "Computer Applications": [
        ("Which SQL clause is used to filter records based on a specified condition?", ["WHERE", "ORDER BY", "GROUP BY", "SELECT"], 0, "The WHERE clause filters rows meeting boolean predicate criteria.", "Easy"),
        ("What does the 'S' stand for in HTTPS?", ["Secure (utilizing SSL/TLS encryption)", "Standard", "Server", "System"], 0, "HTTPS uses Transport Layer Security (TLS/SSL) encryption for authentic, eavesdropping-resistant communications.", "Easy"),
        ("Which HTML5 element is used to define navigation links?", ["<nav>", "<header>", "<section>", "<aside>"], 0, "The <nav> semantic element wraps major site navigation link blocks.", "Easy")
    ],
    "Applied Mathematics": [
        ("What is the formula for the Equated Monthly Installment (EMI) on a loan?", ["E = [P × r × (1+r)ⁿ] / [(1+r)ⁿ - 1]", "E = P × r × n", "E = (P + r) / n", "E = P / (r × n)"], 0, "The standard financial loan amortisation formula is E = P · r · (1+r)ⁿ / ((1+r)ⁿ - 1).", "Medium"),
        ("In profit optimization, what first-order condition must hold at maximum profit?", ["Marginal Revenue equals Marginal Cost (MR = MC)", "Total Revenue = 0", "Average Cost is maximized", "Marginal Revenue = 0"], 0, "Profit π(q) = TR(q) - TC(q) is maximized when dπ/dq = MR - MC = 0, meaning MR = MC.", "Medium"),
        ("In modular arithmetic, what is 27 mod 4?", ["3", "1", "2", "0"], 0, "27 = 4 × 6 + 3, leaving a remainder of 3.", "Easy")
    ],
    "Psychology": [
        ("Who formulated the Classical Conditioning paradigm using experiments with dogs?", ["Ivan Pavlov", "B.F. Skinner", "Sigmund Freud", "Jean Piaget"], 0, "Russian physiologist Ivan Pavlov discovered conditioned reflexes (Salivation to bell chime).", "Easy"),
        ("Which stage model of memory posits Sensory Memory, Short-Term Memory, and Long-Term Memory?", ["Atkinson-Shiffrin Model", "Levels of Processing (Craik & Lockhart)", "Working Memory Model (Baddeley)", "Dual Coding Theory"], 0, "Richard Atkinson and Richard Shiffrin proposed the multi-store memory model in 1968.", "Medium")
    ],
    "Sociology": [
        ("Who coined the term 'Sociological Imagination'?", ["C. Wright Mills", "Max Weber", "Karl Marx", "Emile Durkheim"], 0, "C. Wright Mills described sociological imagination as the awareness of the relationship between individual experience and the wider society.", "Easy"),
        ("What is a 'Primary Group' in sociological terms?", ["Small, intimate, face-to-face social group (e.g. family)", "A large corporation", "A national political party", "A trade union"], 0, "Charles Cooley defined primary groups as tightly knit, emotionally bonded associations like family.", "Easy")
    ],
    "Legal Studies": [
        ("Which article of the Indian Constitution empowers the Supreme Court to issue prerogative writs for enforcement of Fundamental Rights?", ["Article 32", "Article 21", "Article 14", "Article 370"], 0, "Article 32 guarantees the Right to Constitutional Remedies, called the heart and soul of the Constitution.", "Easy"),
        ("What is the primary objective of Lok Adalats in India?", ["To provide amicable, expeditious, and cost-free dispute resolution", "To prosecute criminal trials", "To amend the constitution", "To regulate banking interest"], 0, "Lok Adalats offer informal, non-adversarial dispute resolution under the Legal Services Authorities Act.", "Easy")
    ],
    "Commercial Studies": [
        ("Which market facilitates the issuance of new securities directly from issuers to investors?", ["Primary Market", "Secondary Market", "Commodity Market", "Money Market"], 0, "The Primary Market deals with Initial Public Offerings (IPOs) where new securities are created and sold.", "Easy"),
        ("What is the primary role of the Securities and Exchange Board of India (SEBI)?", ["To protect the interests of investors and regulate securities markets", "To print currency notes", "To collect income tax", "To manage commercial bank deposits"], 0, "SEBI is the statutory regulatory body governing securities and commodities markets in India.", "Easy")
    ]
}

