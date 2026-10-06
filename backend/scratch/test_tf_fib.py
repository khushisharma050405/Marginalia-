import sys
sys.path.insert(0, '/Users/khushisharma/Desktop/Marginalia/backend')
import random

def gen_curriculum_tf_question(topic_name: str, chapter_name: str, subject_name: str, class_level: str, difficulty: str = "Medium"):
    low_t = (topic_name or "").lower()
    low_ch = (chapter_name or "").lower()
    low_s = (subject_name or "").lower()

    tf_pool = []

    # 1. Computer Science & AI
    if any(k in low_s for k in ["computer", "ai", "artificial", "it", "python", "computational"]):
        tf_pool.extend([
            ("State True or False: In computational thinking, decomposition refers to breaking down a complex problem into smaller, manageable parts.", "True", ["False"], "True. Decomposition divides complex systems or challenges into smaller sub-components for easier problem solving.", "Easy"),
            ("State True or False: In Python, a tuple is mutable and elements can be re-assigned after initialization.", "False", ["True"], "False. Tuples are immutable sequence types in Python; attempting item assignment raises a TypeError.", "Easy"),
            ("State True or False: In standard flowcharts, a diamond symbol represents a decision or conditional test branching.", "True", ["False"], "True. Diamond symbols denote conditional operations (e.g. Yes/No, True/False).", "Easy"),
            ("State True or False: The three primary technical domains of AI are Data Science, Computer Vision, and Natural Language Processing.", "True", ["False"], "True. AI applications are categorized into Data Science, Computer Vision (CV), and NLP.", "Easy"),
            ("State True or False: The 4Ws Problem Canvas in AI project scoping stands for Who, What, Where, and Why.", "True", ["False"], "True. The 4Ws canvas systematically frames the problem stakeholders, context, and impact.", "Easy"),
            ("State True or False: Binary search can be executed directly on an unsorted array without prior sorting.", "False", ["True"], "False. Binary search strictly requires the sequence of elements to be sorted monotonically.", "Medium"),
            ("State True or False: In computing, exactly 8 bits make up one byte.", "True", ["False"], "True. One byte is universally defined as a collection of 8 bits.", "Easy"),
            ("State True or False: An HC-SR04 ultrasonic sensor measures distance by calculating the time-of-flight of high-frequency sound waves.", "True", ["False"], "True. Ultrasonic sensors calculate distance = (time × speed of sound) / 2.", "Medium")
        ])

    # 2. Science (Physics, Chemistry, Biology, EVS)
    elif any(k in low_s for k in ["science", "physics", "chem", "bio", "evs", "environment"]):
        tf_pool.extend([
            ("State True or False: Mitochondria are known as the powerhouse of the cell because they synthesize ATP.", "True", ["False"], "True. Mitochondria produce cellular energy through aerobic respiration.", "Easy"),
            ("State True or False: Blue litmus paper turns red when introduced into an acidic solution.", "True", ["False"], "True. Acids turn blue litmus red, whereas bases turn red litmus blue.", "Easy"),
            ("State True or False: According to the Law of Conservation of Mass, matter can be created and destroyed during chemical reactions.", "False", ["True"], "False. Mass can neither be created nor destroyed in a chemical reaction; total mass is conserved.", "Easy"),
            ("State True or False: The SI unit of force is the Newton (N).", "True", ["False"], "True. Force is measured in Newtons (N) where 1 N = 1 kg·m/s².", "Easy"),
            ("State True or False: Sound waves can propagate through a complete physical vacuum.", "False", ["True"], "False. Sound requires a mechanical material medium (solid, liquid, or gas) to travel.", "Easy"),
            ("State True or False: Photosynthesis in green plants takes place inside chloroplasts containing chlorophyll.", "True", ["False"], "True. Chloroplasts contain chlorophyll pigments that absorb photon energy from sunlight.", "Easy"),
            ("State True or False: Pure distilled water at 25°C has a neutral pH of exactly 7.", "True", ["False"], "True. At 25°C, pure water has [H+] = [OH-] = 10^-7 M, corresponding to pH 7.", "Easy")
        ])

    # 3. Social Science
    elif any(k in low_s for k in ["social", "sst", "hist", "geo", "civic", "pol", "eco"]):
        tf_pool.extend([
            ("State True or False: Dr. B.R. Ambedkar was the Chairman of the Drafting Committee of the Constituent Assembly.", "True", ["False"], "True. Dr. B.R. Ambedkar served as the chief architect and Drafting Committee Chairman.", "Easy"),
            ("State True or False: Mahatma Gandhi inaugurated the Civil Disobedience Movement with the Dandi Salt March in 1930.", "True", ["False"], "True. The historic Dandi March occurred in March-April 1930.", "Easy"),
            ("State True or False: Under Universal Adult Franchise in India, the minimum voting age is 21 years.", "False", ["True"], "False. The 61st Constitutional Amendment Act reduced the voting age to 18 years.", "Easy"),
            ("State True or False: The Godavari is the longest river system in Peninsular India, often called 'Dakshin Ganga'.", "True", ["False"], "True. The Godavari river is the largest river in Peninsular India.", "Easy"),
            ("State True or False: The primary sector of the economy includes manufacturing factories and heavy industries.", "False", ["True"], "False. Manufacturing belongs to the Secondary sector; Primary sector extracts natural resources.", "Easy"),
            ("State True or False: Black soil is also called Regur soil and has high moisture retention ideal for cotton.", "True", ["False"], "True. Regur soil in the Deccan trap is clayey and ideal for cotton cultivation.", "Easy")
        ])

    # 4. English
    elif "english" in low_s:
        tf_pool.extend([
            ("State True or False: In the sentence 'The brave girl ran quickly', the word 'quickly' functions as an adverb.", "True", ["False"], "True. 'Quickly' modifies the verb 'ran', indicating manner of action.", "Easy"),
            ("State True or False: The words 'Ancient' and 'Modern' are synonyms.", "False", ["True"], "False. 'Ancient' and 'Modern' are direct antonyms (opposites).", "Easy"),
            ("State True or False: In Robert Frost's poem 'Dust of Snow', the crow shakes fine snow from a hemlock tree onto the poet.", "True", ["False"], "True. The unexpected snow from the hemlock tree lifts the poet's mood.", "Easy"),
            ("State True or False: The sentence 'A beautiful song was sung by her' is written in the passive voice.", "True", ["False"], "True. The grammatical subject receives the action performed by the agent.", "Easy")
        ])

    # 5. Hindi
    elif "hindi" in low_s:
        tf_pool.extend([
            ("बताइए सही या गलत: किसी व्यक्ति, वस्तु, स्थान या भाव के नाम को संज्ञा कहते हैं।", "True", ["False"], "सही। किसी भी व्यक्ति, प्राणी, स्थान या भाव के नाम को संज्ञा कहा जाता है।", "Easy"),
            ("बताइए सही या गलत: 'दिन' का विलोम शब्द 'प्रकाश' होता है।", "False", ["True"], "गलत। 'दिन' का विपरीत (विलोम) शब्द 'रात' होता है।", "Easy"),
            ("बताइए सही या गलत: 'आँखों का तारा' मुहावरे का अर्थ अत्यधिक प्यारा होना है।", "True", ["False"], "सही। 'आँखों का तारा' अत्यधिक प्रिय व्यक्ति के लिए प्रयुक्त होता है।", "Easy"),
            ("बताइए सही या गलत: 'सूर्योदय' शब्द गुण स्वर संधि का उदाहरण है।", "True", ["False"], "सही। सूर्य + उदय (अ + उ = ओ) गुण स्वर संधि का निर्माण करता है।", "Easy")
        ])

    # 6. Mathematics (Default / Math)
    else:
        tf_pool.extend([
            ("State True or False: The sum of all three interior angles in any triangle is always 180°.", "True", ["False"], "True. The angle sum property of any Euclidean triangle guarantees the total is 180°.", "Easy"),
            ("State True or False: The sum of all interior angles of any convex quadrilateral is 360°.", "True", ["False"], "True. Dividing a quadrilateral into two triangles gives 2 × 180° = 360°.", "Easy"),
            ("State True or False: In the Indian numeral system, 1 crore equals 100 lakhs.", "True", ["False"], "True. 1 Crore = 1,00,00,000 = 100 × 1,00,000 (100 lakhs).", "Easy"),
            ("State True or False: An angle measuring exactly 90 degrees is called an acute angle.", "False", ["True"], "False. An angle measuring exactly 90° is a right angle; acute angles are strictly less than 90°.", "Easy"),
            ("State True or False: Zero (0) is the additive identity for all rational numbers.", "True", ["False"], "True. For any rational number a, a + 0 = 0 + a = a.", "Easy"),
            ("State True or False: Rational numbers are closed under division by zero.", "False", ["True"], "False. Division by zero is undefined; rational numbers are not closed under division.", "Medium")
        ])

    if tf_pool:
        picked = random.choice(tf_pool)
        return picked[0], picked[1], picked[2], picked[3], picked[4]
    return None

print('Test TF:', gen_curriculum_tf_question('AI', 'AI', 'Computational Thinking & AI', '6'))
