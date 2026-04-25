# Barcha fanlar bo'yicha savollar
# Format: { "savol": "...", "options": [...], "correct": 0-3, "explanation": "..." }

QUESTIONS = {

    "matematika": [
        {
            "question": "2³ × 2⁴ = ?",
            "options": ["2⁷", "2¹²", "4⁷", "2⁶"],
            "correct": 0,
            "explanation": "Bir xil asosli darajalar ko'paytirilganda, ko'rsatkichlar qo'shiladi: 2³⁺⁴ = 2⁷"
        },
        {
            "question": "√144 = ?",
            "options": ["11", "12", "13", "14"],
            "correct": 1,
            "explanation": "12 × 12 = 144, shuning uchun √144 = 12"
        },
        {
            "question": "Agar x + 5 = 12 bo'lsa, x = ?",
            "options": ["5", "6", "7", "8"],
            "correct": 2,
            "explanation": "x = 12 - 5 = 7"
        },
        {
            "question": "Uchburchak burchaklari yig'indisi necha daraja?",
            "options": ["90°", "180°", "270°", "360°"],
            "correct": 1,
            "explanation": "Har qanday uchburchak burchaklari yig'indisi 180° ga teng"
        },
        {
            "question": "15% of 200 = ?",
            "options": ["25", "30", "35", "40"],
            "correct": 1,
            "explanation": "200 × 0.15 = 30"
        },
        {
            "question": "(-3)² = ?",
            "options": ["-9", "-6", "6", "9"],
            "correct": 3,
            "explanation": "(-3)² = (-3) × (-3) = 9. Manfiy sonning juft darajasi musbat"
        },
        {
            "question": "log₁₀(1000) = ?",
            "options": ["2", "3", "4", "10"],
            "correct": 1,
            "explanation": "10³ = 1000, shuning uchun log₁₀(1000) = 3"
        },
        {
            "question": "Doira yuzi formulasi?",
            "options": ["2πr", "πr²", "πd", "2πr²"],
            "correct": 1,
            "explanation": "Doira yuzi S = πr², bu yerda r - radius"
        },
        {
            "question": "1/3 + 1/6 = ?",
            "options": ["1/2", "2/9", "1/4", "2/6"],
            "correct": 0,
            "explanation": "1/3 = 2/6, 2/6 + 1/6 = 3/6 = 1/2"
        },
        {
            "question": "Arifmetik progressiya: 2, 5, 8, 11... Keyingi son?",
            "options": ["12", "13", "14", "15"],
            "correct": 2,
            "explanation": "Farq d = 3. 11 + 3 = 14"
        },
    ],

    "ingliz": [
        {
            "question": "Choose the correct form: 'She ___ to school every day.'",
            "options": ["go", "goes", "going", "gone"],
            "correct": 1,
            "explanation": "She (3rd person singular) bilan Present Simple da goes ishlatiladi"
        },
        {
            "question": "'Beautiful' so'zining antonimi nima?",
            "options": ["Ugly", "Pretty", "Lovely", "Nice"],
            "correct": 0,
            "explanation": "Beautiful (go'zal) so'zining antonimi Ugly (xunuk)"
        },
        {
            "question": "'I have been studying for 3 hours.' — Bu qaysi zamon?",
            "options": ["Present Simple", "Past Perfect", "Present Perfect Continuous", "Past Continuous"],
            "correct": 2,
            "explanation": "Have been + V-ing = Present Perfect Continuous. Uzoq vaqtdan beri davom etayotgan harakat"
        },
        {
            "question": "What is the plural of 'child'?",
            "options": ["Childs", "Childes", "Children", "Childrens"],
            "correct": 2,
            "explanation": "Child ning ko'pligi noto'g'ri shakl — Children"
        },
        {
            "question": "'Enormous' so'zining ma'nosi?",
            "options": ["Kichik", "O'rtacha", "Ulkan", "Qadimiy"],
            "correct": 2,
            "explanation": "Enormous = very large = ulkan, katta"
        },
        {
            "question": "Choose the correct article: '___ Eiffel Tower is in Paris.'",
            "options": ["A", "An", "The", "No article"],
            "correct": 2,
            "explanation": "Noyob ob'ektlar oldidan 'The' ishlatiladi"
        },
        {
            "question": "'She suggested ___ to the cinema.' — To'g'ri forma?",
            "options": ["go", "to go", "going", "went"],
            "correct": 2,
            "explanation": "Suggest + V-ing: 'suggested going'"
        },
        {
            "question": "What does 'procrastinate' mean?",
            "options": ["Tez bajarmoq", "Kechiktirmoq", "Unutmoq", "Yangilash"],
            "correct": 1,
            "explanation": "Procrastinate = to delay or postpone = kechiktirmoq, vaqtni o'tkazib yubormoq"
        },
        {
            "question": "Passive voice: 'They built this house in 1990.' →",
            "options": [
                "This house is built in 1990.",
                "This house was built in 1990.",
                "This house has been built in 1990.",
                "This house had built in 1990."
            ],
            "correct": 1,
            "explanation": "Past Simple Passive: was/were + V3. 'was built' to'g'ri"
        },
        {
            "question": "Choose the correct preposition: 'I'm good ___ mathematics.'",
            "options": ["in", "at", "on", "for"],
            "correct": 1,
            "explanation": "Good at = biror narsada yaxshi. 'good at mathematics'"
        },
    ],

    "ozbek": [
        {
            "question": "'Mehribon' so'zining sinonimi?",
            "options": ["Shafqatsiz", "Rahmdil", "Befarq", "Qo'pol"],
            "correct": 1,
            "explanation": "Mehribon = rahmdil, saxiy, xayrixoh"
        },
        {
            "question": "Quyidagi so'zlardan qaysi biri ot turkumiga kiradi?",
            "options": ["Yashil", "Yugurmoq", "Baxt", "Tez"],
            "correct": 2,
            "explanation": "Baxt — ot (predmet, hodisa, tushunchani bildiradi)"
        },
        {
            "question": "O'zbek alifbosida nechta harf bor?",
            "options": ["26", "29", "32", "35"],
            "correct": 1,
            "explanation": "Lotin yozuviga asoslangan zamonaviy O'zbek alifbosida 29 ta harf bor"
        },
        {
            "question": "'Kitob o'qidim' gapida 'o'qidim' so'zi qaysi zamon?",
            "options": ["Hozirgi zamon", "O'tgan zamon", "Kelasi zamon", "Buyruq mayli"],
            "correct": 1,
            "explanation": "-di qo'shimchasi o'tgan zamon aniq shaklini hosil qiladi"
        },
        {
            "question": "Qaysi qatorda imlo xatosi bor?",
            "options": ["Rahmat", "Sog'liq", "Maktab", "Kitob"],
            "correct": 1,  # Actually all correct, this is a trick
            "explanation": "Barcha so'zlar to'g'ri yozilgan — bu savol diqqatni sinaydi!"
        },
        {
            "question": "'Toshkent' so'zi qaysi tildagi so'zlardan tashkil topgan?",
            "options": ["Fors-tojik", "Arabcha", "Turkiy", "Ruscha"],
            "correct": 0,
            "explanation": "Tosh (tojikcha 'tosh') + kent (tojikcha 'shahar') = Toshkent"
        },
        {
            "question": "Fe'lning noaniq shakli qanday yasaladi?",
            "options": ["-di qo'shimchasi", "-moq qo'shimchasi", "-ydi qo'shimchasi", "-ish qo'shimchasi"],
            "correct": 1,
            "explanation": "Fe'lning noaniq shakli -moq qo'shimchasi yordamida yasaladi: yurmoq, o'qimoq"
        },
        {
            "question": "Quyidagilardan qaysi biri murakkab gap?",
            "options": [
                "Bola o'ynadi.",
                "Qush uchdi.",
                "Men kitob o'qidim, u esa uxladi.",
                "Gul chiroyli."
            ],
            "correct": 2,
            "explanation": "Murakkab gap ikki va undan ortiq sodda gapdan tashkil topadi"
        },
    ],

    "kimyo": [
        {
            "question": "Suvning kimyoviy formulasi?",
            "options": ["CO₂", "H₂O", "NaCl", "O₂"],
            "correct": 1,
            "explanation": "Suv — 2 ta vodorod va 1 ta kislorod atomi: H₂O"
        },
        {
            "question": "Davriy sistemada birinchi element?",
            "options": ["Geliy", "Litiy", "Vodorod", "Uglerod"],
            "correct": 2,
            "explanation": "Vodorod (H) — atom raqami 1, davriy sistemada birinchi element"
        },
        {
            "question": "NaCl nima?",
            "options": ["Shakar", "Osh tuzi", "Soda", "Sirka"],
            "correct": 1,
            "explanation": "NaCl = Natriy xlorid = osh tuzi"
        },
        {
            "question": "Eng yengil gaz?",
            "options": ["Kislorod", "Azot", "Vodorod", "Geliy"],
            "correct": 2,
            "explanation": "Vodorod (H₂) — eng yengil gaz, zichligi 0.0899 g/L"
        },
        {
            "question": "pH = 7 nima bildiradi?",
            "options": ["Kislotali", "Neytral", "Ishqoriy", "Oksidlangan"],
            "correct": 1,
            "explanation": "pH = 7 neytral muhitni bildiradi. pH < 7 kislotali, pH > 7 ishqoriy"
        },
        {
            "question": "CO₂ qanday gaz?",
            "options": ["Kislorod", "Vodorod", "Uglerod dioksid", "Azot oksid"],
            "correct": 2,
            "explanation": "CO₂ = Carbon dioxide = Uglerod dioksid (karbonat angidrid)"
        },
        {
            "question": "Oltin elementining belgisi?",
            "options": ["Go", "Gd", "Au", "Ag"],
            "correct": 2,
            "explanation": "Oltin — Au (Aurum — lotincha). Ag esa kumush (Argentum)"
        },
        {
            "question": "Avogadro soni taxminan necha?",
            "options": ["6.02 × 10²³", "3.14 × 10¹⁰", "9.8 × 10²", "1.6 × 10⁻¹⁹"],
            "correct": 0,
            "explanation": "Avogadro soni NA = 6.02 × 10²³ mol⁻¹"
        },
    ],

    "biologiya": [
        {
            "question": "Fotosintez qayerda sodir bo'ladi?",
            "options": ["Mitoxondriya", "Yadro", "Xloroplast", "Ribosoma"],
            "correct": 2,
            "explanation": "Fotosintez xloroplastlarda, aniqrog'i tilakoidlarda sodir bo'ladi"
        },
        {
            "question": "DNK to'liq nomi?",
            "options": [
                "Dinamik Nuklein Kislota",
                "Dezoksiribonuklein kislota",
                "Ribonuklein kislota",
                "Dinuklein kislota"
            ],
            "correct": 1,
            "explanation": "DNK = Dezoksiribonuklein kislota — irsiyat ma'lumotlarini saqlaydi"
        },
        {
            "question": "Inson organizmida nechta xromosoma bor?",
            "options": ["23", "44", "46", "48"],
            "correct": 2,
            "explanation": "Inson hujayralarida 46 ta xromosoma (23 juft) bo'ladi"
        },
        {
            "question": "Qon guruhlarining nechta turi bor (ABO tizimi)?",
            "options": ["2", "3", "4", "5"],
            "correct": 2,
            "explanation": "ABO tizimida 4 ta qon guruhi: I(O), II(A), III(B), IV(AB)"
        },
        {
            "question": "Eng katta hujayra organoidasi?",
            "options": ["Ribosoma", "Mitoxondriya", "Yadro", "Lizosoma"],
            "correct": 2,
            "explanation": "Yadro — hujayraning eng katta organoidasi, DNK saqlanadi"
        },
        {
            "question": "Fotosintez tenglamasi: 6CO₂ + 6H₂O + yorug'lik → ?",
            "options": ["C₆H₁₂O₆ + 6O₂", "6CO + H₂O", "C₆H₁₂ + O₂", "CO₂ + H₂"],
            "correct": 0,
            "explanation": "Fotosintez natijasida glyukoza (C₆H₁₂O₆) va kislorod (O₂) hosil bo'ladi"
        },
        {
            "question": "Odam yuragining normal urish chastotasi?",
            "options": ["40-50", "60-80", "100-120", "120-140"],
            "correct": 1,
            "explanation": "Normal yurak urish chastotasi minutiga 60-80 marta"
        },
    ],

    "fizika": [
        {
            "question": "Yorug'lik tezligi taxminan qancha?",
            "options": ["3 × 10⁶ m/s", "3 × 10⁸ m/s", "3 × 10¹⁰ m/s", "3 × 10⁴ m/s"],
            "correct": 1,
            "explanation": "Yorug'lik tezligi c ≈ 3 × 10⁸ m/s (300,000 km/s)"
        },
        {
            "question": "Nyutonning ikkinchi qonuni formulasi?",
            "options": ["F = mv", "F = ma", "F = m/a", "F = v/t"],
            "correct": 1,
            "explanation": "F = ma: Kuch = massa × tezlanish"
        },
        {
            "question": "Ohm qonuni formulasi?",
            "options": ["U = IR", "I = UR", "R = UI", "P = UI"],
            "correct": 0,
            "explanation": "U = IR: Kuchlanma = tok × qarshilik"
        },
        {
            "question": "Erkin tushish tezlanishi (g) taxminan?",
            "options": ["9.8 m/s²", "10.8 m/s²", "8.9 m/s²", "11 m/s²"],
            "correct": 0,
            "explanation": "g ≈ 9.8 m/s² (amalda ko'pincha 10 m/s² deb olinadi)"
        },
        {
            "question": "1 kVt = ?",
            "options": ["10 Vt", "100 Vt", "1000 Vt", "10000 Vt"],
            "correct": 2,
            "explanation": "1 kilovat = 1000 vat"
        },
        {
            "question": "Issiqlikning asosiy o'lchov birligi?",
            "options": ["Vatt", "Njuton", "Joule", "Pascal"],
            "correct": 2,
            "explanation": "Energiya va issiqlik Joule (J) da o'lchanadi"
        },
        {
            "question": "Tovush to'lqini qanday to'lqin?",
            "options": ["Ko'ndalang", "Bo'ylama", "Elektromagnit", "Kvant"],
            "correct": 1,
            "explanation": "Tovush to'lqini bo'ylama (longitudinal) to'lqin hisoblanadi"
        },
    ],

    "geografiya": [
        {
            "question": "Dunyodagi eng uzun daryo?",
            "options": ["Amazon", "Nil", "Yantszi", "Missisipi"],
            "correct": 1,
            "explanation": "Nil daryosi — 6650 km bilan dunyodagi eng uzun daryo"
        },
        {
            "question": "O'zbekistonning poytaxti?",
            "options": ["Samarqand", "Buxoro", "Toshkent", "Namangan"],
            "correct": 2,
            "explanation": "Toshkent — O'zbekiston Respublikasining poytaxti"
        },
        {
            "question": "Dunyodagi eng katta okean?",
            "options": ["Atlantika", "Hind", "Tinch", "Arktika"],
            "correct": 2,
            "explanation": "Tinch okean (Pacific) — 165 mln km² bilan eng katta okean"
        },
        {
            "question": "Everest tog'i qayerda joylashgan?",
            "options": ["Hindiston", "Xitoy-Nepal chegarasi", "Tibet", "Pakistan"],
            "correct": 1,
            "explanation": "Everest (8848 m) Xitoy va Nepal chegarasida joylashgan"
        },
        {
            "question": "O'zbekiston nechanchi yili mustaqillik oldi?",
            "options": ["1989", "1990", "1991", "1992"],
            "correct": 2,
            "explanation": "O'zbekiston 1991-yil 1-sentabrda mustaqilligini e'lon qildi"
        },
        {
            "question": "Yer shari ekvatorining uzunligi taxminan?",
            "options": ["20,000 km", "30,000 km", "40,000 km", "50,000 km"],
            "correct": 2,
            "explanation": "Yer ekvatorining uzunligi ≈ 40,075 km"
        },
        {
            "question": "Amudaryo qayerga quyiladi?",
            "options": ["Kaspiy dengizi", "Orol dengizi", "Qora dengiz", "Fors ko'rfazi"],
            "correct": 1,
            "explanation": "Amudaryo Orol dengiziga quyiladi (hozir deyarli qurib ketgan)"
        },
    ],

    "tarix": [
        {
            "question": "Amir Temur qaysi yili tug'ilgan?",
            "options": ["1320", "1336", "1350", "1370"],
            "correct": 1,
            "explanation": "Amir Temur (Tamerlane) 1336-yil 9-aprelda Kesh (Shahrisabz)da tug'ilgan"
        },
        {
            "question": "Birinchi jahon urushi qachon boshlandi?",
            "options": ["1912", "1914", "1916", "1918"],
            "correct": 1,
            "explanation": "Birinchi jahon urushi 1914-yil 28-iyulda boshlandi"
        },
        {
            "question": "Ipak yo'li qaysi shaharlar orqali o'tgan?",
            "options": [
                "Rim-Hindiston",
                "Xitoy-O'rta dengiz",
                "Misr-Arabiston",
                "Rossiya-Xitoy"
            ],
            "correct": 1,
            "explanation": "Buyuk Ipak yo'li Xitoydan O'rta dengizgacha cho'zilgan"
        },
        {
            "question": "Al-Xorazmiy qaysi asarda algebra faniga asos soldi?",
            "options": ["Al-Qonun", "Al-jabr", "Ziji Ko'ragoniy", "Kitob ul-hisob"],
            "correct": 1,
            "explanation": "'Al-jabr val-muqobala' — algebra fanining asoschisi bo'lgan asar"
        },
        {
            "question": "Sovet Ittifoqi qaysi yili parchalandi?",
            "options": ["1989", "1990", "1991", "1992"],
            "correct": 2,
            "explanation": "SSSR rasman 1991-yil 25-dekabrda tarqaldi"
        },
        {
            "question": "Samarqandda qaysi sulola hukmronlik qilgan?",
            "options": ["Somoniylar", "Temuriylar", "Qoraxoniylar", "Shayboniylar"],
            "correct": 1,
            "explanation": "Temuriylar sulolasi (1370-1500) davrida Samarqand poytaxt bo'lgan"
        },
    ],

    "informatika": [
        {
            "question": "1 bayt necha bitdan iborat?",
            "options": ["4", "8", "16", "32"],
            "correct": 1,
            "explanation": "1 bayt = 8 bit. Bu standart o'lchov birligi"
        },
        {
            "question": "WWW nima?",
            "options": ["World Wide Web", "Wide World Web", "Web World Wide", "World Web Wire"],
            "correct": 0,
            "explanation": "WWW = World Wide Web — 1991-yilda Tim Berners-Lee tomonidan yaratilgan"
        },
        {
            "question": "Python qanday til?",
            "options": ["Kompilyatsiya", "Interpretatsiya", "Assembly", "Mashina"],
            "correct": 1,
            "explanation": "Python — interpretatsiya qilinadigan yuqori darajali dasturlash tili"
        },
        {
            "question": "CPU nima?",
            "options": [
                "Central Processing Unit",
                "Computer Power Unit",
                "Central Power Unit",
                "Computer Processing Unit"
            ],
            "correct": 0,
            "explanation": "CPU = Central Processing Unit = Markaziy protsessor"
        },
        {
            "question": "HTML nima uchun ishlatiladi?",
            "options": ["Dastur yozish", "Veb-sahifalar yaratish", "Ma'lumotlar bazasi", "Tarmoq sozlash"],
            "correct": 1,
            "explanation": "HTML (HyperText Markup Language) — veb-sahifalar tuzilmasini yaratish uchun"
        },
        {
            "question": "Binary sanoq sistemasida 1010 = ?",
            "options": ["8", "10", "12", "14"],
            "correct": 1,
            "explanation": "1010₂ = 1×8 + 0×4 + 1×2 + 0×1 = 8+2 = 10₁₀"
        },
        {
            "question": "RAM nima?",
            "options": ["Doimiy xotira", "Operativ xotira", "Tashqi xotira", "Virtual xotira"],
            "correct": 1,
            "explanation": "RAM = Random Access Memory = Operativ (tasodifiy kirish) xotira"
        },
        {
            "question": "Git qanday tizim?",
            "options": ["Operatsion tizim", "Versiyalarni boshqarish tizimi", "Ma'lumotlar bazasi", "Veb-server"],
            "correct": 1,
            "explanation": "Git — Linus Torvalds yaratgan distributed version control system"
        },
    ],
}
