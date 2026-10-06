import re

# 1. Official Class 6 NCERT 2024-2026 NCF-SE Chapters
CLASS_6_ACCURATE = {
    'Mathematics': [
        ('Patterns in Mathematics', ['Shapes and number patterns', 'Visual patterns and sequences', 'Rules of patterns']),
        ('Lines and Angles', ['Points, lines, rays, line segments', 'Measuring angles with protractor', 'Types: acute, right, obtuse, straight', 'Parallel and intersecting lines']),
        ('Number Play', ['Factors and multiples', 'Prime and composite numbers', 'Divisibility rules (2, 3, 4, 5, 6, 8, 9, 10, 11)', 'HCF and LCM techniques']),
        ('Data Handling and Presentation', ['Collecting and organizing data', 'Tally marks tables', 'Pictographs and bar graphs', 'Interpreting graphical trends']),
        ('Prime Time', ['Prime factorisation', 'Factor trees', 'Co-prime numbers', 'Applications of prime numbers']),
        ('Perimeter and Area', ['Perimeter of regular polygons', 'Perimeter of rectangle and square', 'Area on square grid', 'Word problems on fencing and flooring']),
        ('Fractions', ['Fractions on the number line', 'Proper, improper and mixed fractions', 'Equivalent fractions and simplest form', 'Addition and subtraction of fractions']),
        ('Playing with Constructions', ['Constructing circles with compass', 'Constructing perpendicular bisectors', 'Constructing angles of 60°, 90°, 120°', 'Angle bisector']),
        ('Symmetry', ['Line of symmetry (reflectional)', 'Symmetrical figures in nature and geometry', 'Multiple lines of symmetry', 'Kaleidoscope and reflection']),
        ('The Other Side of Zero', ['Concept of negative numbers', 'Integers on the number line', 'Ordering and comparing integers', 'Addition and subtraction of integers'])
    ],
    'Science': [
        ('The Wonderful World of Science', ['What is science and scientific enquiry', 'Observing, hypothesizing and experimenting', 'Science in everyday life and curiosity']),
        ('Diversity in the Living World', ['Classification of living organisms', 'Plant diversity: herbs, shrubs, trees', 'Animal diversity: terrestrial, aquatic, aerial', 'Habitats and adaptations']),
        ('Mindful Eating: A Path to a Healthy Body', ['Essential nutrients: carbs, proteins, fats, vitamins, minerals', 'Dietary fibre and water', 'Balanced diet for growing adolescents', 'Deficiency diseases and prevention']),
        ('Exploring Magnets', ['Discovery of magnets and magnetic materials', 'Poles of a magnet: North and South', 'Magnetic attraction and repulsion laws', 'Making simple magnets and compass usage']),
        ('Measurement of Length and Motion', ['Standard units of measurement (SI system)', 'Measuring length with meter scale', 'Types of motion: rectilinear, circular, periodic', 'Importance of precision in measurement']),
        ('Materials Around Us', ['Properties of materials: appearance, hardness, lustre', 'Solubility in water (soluble vs insoluble)', 'Density: floating vs sinking', 'Transparency: transparent, translucent, opaque']),
        ('Temperature and its Measurement', ['Concept of heat and hotness', 'Clinical vs laboratory thermometers', 'Reading temperature in Celsius and Fahrenheit', 'Precautions when measuring temperature']),
        ('A Journey through States of Water', ['Three states of water: ice, water, water vapour', 'Evaporation, condensation and precipitation', 'The natural water cycle', 'Conserving fresh water resources']),
        ('Methods of Separation in Everyday Life', ['Handpicking, threshing and winnowing', 'Sedimentation, decantation and filtration', 'Evaporation and distillation', 'Separating mixtures with multiple methods']),
        ('Living Creatures: Exploring their Characteristics', ['Characteristics of living things: respiration, nutrition, growth', 'Response to stimuli and excretion', 'Reproduction in plants and animals', 'Cellular structure basics']),
        ('Nature’s Treasures', ['Renewable vs non-renewable resources', 'Forests, soil, minerals and wildlife', 'Air and water as life-supporting treasures', 'Sustainable use and conservation practices']),
        ('Beyond Earth', ['The Solar System and eight planets', 'Moon, moon phases and tides', 'Stars, constellations (Ursa Major, Orion)', 'Space exploration and Indian satellite missions'])
    ],
    'Social Science (SST)': [
        ('Locating Places on the Earth', ['Latitudes and parallels', 'Longitudes and meridians', 'Equator, tropics and polar circles', 'Locating coordinates on globes']),
        ('Oceans and Continents', ['Seven continents: physical features and sizes', 'Five major oceans of the world', 'Interconnectedness of ocean currents and marine life', 'Human settlement across landmasses']),
        ('Landforms and Life', ['Mountains, plateaus, and plains', 'How landforms shape human occupations and culture', 'Major landforms of India', 'Natural hazards and environmental balance']),
        ('Timeline and Sources of History', ['Understanding BCE and CE timeline', 'Archaeological sources: pottery, coins, inscriptions', 'Literary sources: manuscripts and travel accounts', 'How historians reconstruct the past']),
        ('India, That is Bharat', ['Geographical boundaries and subcontinent identity', 'Cultural unity in geographical diversity', 'Ancient names of our country', 'The concept of cultural roots']),
        ('The Beginnings of Indian Civilisation', ['The Harappan (Indus Valley) Civilisation', 'Town planning, citadel, Great Bath and drainage', 'Crafts, seals, trade and occupations', 'Decline and legacy of Harappan culture']),
        ('India’s Cultural Roots', ['Vedic literature and philosophical thoughts', 'Upanishads and the quest for knowledge', 'Teachings of Mahavira (Jainism)', 'Teachings of Gautama Buddha (Buddhism)']),
        ('Unity in Diversity, or "Many in the One"', ['Linguistic diversity across Indian states', 'Diverse culinary and festive traditions', 'Composite Indian cultural fabric', 'Constitutional respect for diversity']),
        ('Family and Community', ['Role of family in personal development', 'Neighborhood cooperation and solidarity', 'Community services and mutual dependence', 'Resolving disputes amicably']),
        ('Grassroots Democracy — Part 1: Governance in Rural Areas', ['The Gram Sabha and its functions', 'Structure of Gram Panchayat: Sarpanch and Ward Members', 'Sources of funds for village development', 'Role of villagers in local self-governance']),
        ('Grassroots Democracy — Part 2: Governance in Urban Areas', ['Municipal Corporation and Municipal Council', 'Ward councillors, committees and commissioner', 'Urban infrastructure: water, sanitation, streetlights', 'Citizen participation in city administration']),
        ('The Value of Work', ['Dignity of labour and respecting all occupations', 'Paid work vs household and care work', 'Gender equality in work opportunities', 'Fair wages and workers’ rights']),
        ('Economic Activities Around Us', ['Primary, secondary, and tertiary sectors', 'Farming, manufacturing, and transport/services', 'Money, markets, and barter system origins', 'Responsible consumer habits'])
    ],
    'English': [
        ('Unit 1: Fables and Folk Tales (A Bottle of Dew & The Raven and the Fox)', ['Reading fluency and comprehension', 'Moral themes: hard work vs trickery', 'Vocabulary and sentence making', 'Nouns and pronouns usage']),
        ('Unit 2: Friendship (Rama to the Rescue & The Friend)', ['Values of true friendship and loyalty', 'Character sketch and descriptive words', 'Adjectives of quality and quantity', 'Informal letter writing']),
        ('Unit 3: Nurturing Nature (The Cherry Tree & The Giving Tree)', ['Environmental appreciation and tree plantation', 'Poetic devices: rhyme and imagery', 'Verb tenses: simple past and present continuous', 'Paragraph writing on nature']),
        ('Unit 4: Sports and Wellness (Change of Heart & The Winner)', ['Sportsmanship, resilience and healthy competition', 'Dialogue writing and role-play', 'Adverbs of manner and time', 'Listening comprehension']),
        ('Unit 5: Culture and Tradition (Hamara Bharat - Incredible India)', ['Indian festivals, arts, and monumental heritage', 'Appreciating regional diversity', 'Conjunctions and prepositions', 'Diary entry writing'])
    ],
    'Hindi': [
        ('मातृभूमि (कविता - सोहनलाल द्विवेदी)', ['देशभक्ति और प्रकृति सौंदर्य का भाव', 'काव्य पाठ और तुकांत शब्द', 'विशेषण और विशेष्य की पहचान', 'पर्यायवाची शब्द']),
        ('गोल (आत्मकथा अंश - मेजर ध्यानचंद)', ['हॉकी के जादूगर की प्रेरक गाथा', 'परिश्रम और खेल भावना', 'वाक्य भेद और विराम चिह्न', 'नए शब्दों का वाक्य प्रयोग']),
        ('तीर्थ यात्रा (कहानी - सुदर्शन)', ['मातृ-प्रेम और मानवीय संवेदना', 'कहानी के मुख्य पात्र और संवाद', 'मुहावरे और उनके अर्थ', 'संज्ञा के भेद']),
        ('हार की जीत (कहानी - सुदर्शन)', ['बाबा भारती और डाकू खड्गसिंह की कहानी', 'हृदय परिवर्तन का संदेश', 'विलोम शब्द और प्रत्यय', 'अनुच्छेद लेखन']),
        ('रहीम के दोहे (नीतिपरक दोहे)', ['रहीम के दोहों का भावार्थ और नीति ज्ञान', 'सत्संगति, परोपकार और वाणी की मिठास', 'कठिन शब्दों के अर्थ', 'दोहा गायन']),
        ('परीक्षा (कहानी - मुंशी प्रेमचंद)', ['दीवान पद के लिए सच्ची परीक्षा', 'दया, परोपकार और निःस्वार्थ सेवा के गुण', 'क्रिया और काल', 'चरित्र चित्रण']),
        ('पेड़ की बात (निबंध - जगदीश चंद्र बोस)', ['पेड़ों में जीवन और संवेदनशीलता', 'वैज्ञानिक दृष्टिकोण और प्रकृति निरीक्षण', 'उपसर्ग और प्रत्यय', 'शुद्ध-अशुद्ध वाक्य']),
        ('सबसे बड़ा मूर्ख (लोककथा)', ['हास्य और बुद्धिमत्ता का समन्वय', 'अकबर-बीरबल की सूझबूझ', 'अनेक शब्दों के लिए एक शब्द', 'संवाद लेखन'])
    ],
    'Sanskrit': [
        ('प्रथमः पाठः - शब्दपरिचयः एवं वन्दना', ['अकारान्त पुल्लिंग शब्दाः (एषः, सः, कः)', 'संस्कृत वर्णमाला एवं उच्चारणम्', 'प्रार्थना श्लोकाः']),
        ('द्वितीयः पाठः - सुभाषितानि एवं नीतिश्लोकाः', ['विद्या, सत्यम् एवं धर्मस्य महत्त्वम्', 'श्लोकार्थः एवं पदच्छेदः', 'समानार्थक शब्दाः']),
        ('तृतीयः पाठः - बकस्य प्रतीकारः एवं मित्रलाभः', ['सियार एवं बगुले की कथा (शृगालः बकः च)', 'अव्‍ययपदानि (यदा, तदा, अपि, च)', 'कथायाः शिक्षा']),
        ('चतुर्थः पाठः - भारतवर्षम् एवं पर्यावरणम्', ['अस्माकं देशः भारतवर्षम्', 'नद्यः, पर्वताः एवं वृक्षाणां रक्षणम्', 'कारकाणि एवं विभक्तयः'])
    ],
    'Computational Thinking & AI': [
        ('Decomposition & Algorithmic Problem Solving', ['Decomposition principles in daily tasks', 'Step-by-step instructions for computers', 'Algorithm flowcharting']),
        ('Pattern Recognition & Logic Design', ['Identifying recurring numerical and spatial patterns', 'Rule induction from data sequences', 'Decision logic: IF-THEN-ELSE']),
        ('Abstraction & Flowcharts', ['Filtering out unnecessary details', 'Standard flowchart symbols (Start, Input, Process, Decision, End)', 'Tracing execution paths']),
        ('Introduction to Artificial Intelligence & Smart Systems', ['Definition of AI and difference from ordinary computing', 'Smart home devices, voice assistants, and robotics', 'Ethical awareness in AI']),
        ('Block Coding & Automation', ['Visual block programming (Scratch/Blockly)', 'Loops, variables, and events', 'Building a basic animated story or interactive quiz'])
    ],
    'French': [
        ('Vous connaissez la France?', ['Geographical map of France, monuments and symbols', 'French flag, cheese, perfumes and currency', 'Greetings: Bonjour, Salut, Au revoir']),
        ('Les Salutations et L’Alphabet', ['French alphabet and accented vowels (é, è, ê, ç)', 'Formal vs informal greetings', 'Counting numbers 1 to 20 in French']),
        ('Les Articles et Les Nombres', ['Definite and indefinite articles (un, une, des, le, la, les)', 'Numbers 21 to 50', 'Basic classroom vocabulary'])
    ]
}

print('Official Class 6 definitions ready.')
