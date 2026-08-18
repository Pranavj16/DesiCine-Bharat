import os
import sys
import django
from datetime import date, time, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from movies.models import Movie, Review
from theaters.models import Theater, Screen, Seat, Showtime
from bookings.models import SnackItem, Booking, BookedSeat, BookingSnack
from payments.models import Payment

def seed_data():
    print("🎬 Seeding 47+ Indian Movies with 100% Unique Official Posters & Precise Themes...")

    # 1. Create Demo Users
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@desicine.in', 'is_staff': True, 'is_superuser': True}
    )
    admin_user.set_password('admin123')
    admin_user.save()

    rahul, _ = User.objects.get_or_create(
        username='rahul_sharma',
        defaults={'email': 'rahul@gmail.com', 'first_name': 'Rahul', 'last_name': 'Sharma'}
    )
    rahul.set_password('password123')
    rahul.save()

    priya, _ = User.objects.get_or_create(
        username='priya_patel',
        defaults={'email': 'priya@gmail.com', 'first_name': 'Priya', 'last_name': 'Patel'}
    )
    priya.set_password('password123')
    priya.save()

    # 2. Rich Indian Movie Collection (47 Films with UNIQUE Official Posters & Strict Theme Tags)
    movies_data = [
        # =========================================================================
        # 1. EDUCATION, STUDENT STRUGGLE, UPSC & MOTIVATIONAL BIOPICS (9 Films)
        # =========================================================================
        {
            "title": "12th Fail",
            "tagline": "Restart! The inspiring journey of a Chambal village boy becoming an IPS officer.",
            "description": "Based on the real-life struggle of Manoj Kumar Sharma, who overcomes extreme poverty, systemic corruption, and personal failures in Chambal to clear the UPSC Civil Services examination and become an honest IPS officer.",
            "genre": "Education, Biographical Drama, Motivational",
            "theme_tags": "education, upsc, student, ias, ips, restart, inspiring, struggle, exam, coaching, civil services",
            "language": "Hindi",
            "certification": "U",
            "duration": 147,
            "rating": 9.2,
            "tomatometer": 98,
            "director": "Vidhu Vinod Chopra",
            "cast": "Vikrant Massey, Medha Shankr, Anant V Joshi, Priyanshu Chatterjee",
            "music_director": "Shantanu Moitra",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2023, 10, 27),
            "poster": "/static/posters/12th_fail.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "3 Idiots",
            "tagline": "Don't chase success, chase excellence and success will follow!",
            "description": "Two friends embark on a road trip to find their lost college friend Rancho, while reminiscing about their hilarious and poignant engineering student days at ICE college under the tyrannical director Virus, learning life lessons about true education vs rote learning.",
            "genre": "Education, Comedy, College Drama",
            "theme_tags": "education, college, engineering, student, friendship, comedy, coming-of-age, inspiring, classroom",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 170,
            "rating": 9.1,
            "tomatometer": 97,
            "director": "Rajkumar Hirani",
            "cast": "Aamir Khan, R. Madhavan, Sharman Joshi, Kareena Kapoor Khan, Boman Irani",
            "music_director": "Shantanu Moitra",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2009, 12, 25),
            "poster": "/static/posters/3_idiots.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Super 30",
            "tagline": "Raja ka beta raja nahi banega, ab raja wahi banega jo haqdaar hoga!",
            "description": "Based on the life of mathematician Anand Kumar from Patna, who runs the famed Super 30 education program, coaching 30 underprivileged aspiring student geniuses every year for the grueling IIT-JEE entrance exam against all corrupt coaching mafia odds.",
            "genre": "Education, Biographical Drama, Inspiring",
            "theme_tags": "education, student, iit, coaching, mathematics, mentorship, inspiring, struggle, exam, teacher",
            "language": "Hindi",
            "certification": "U",
            "duration": 154,
            "rating": 8.4,
            "tomatometer": 88,
            "director": "Vikas Bahl",
            "cast": "Hrithik Roshan, Mrunal Thakur, Nandish Sandhu, Pankaj Tripathi",
            "music_director": "Ajay-Atul",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2019, 7, 12),
            "poster": "/static/posters/super_30.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Taare Zameen Par",
            "tagline": "Every child is special. A heartwarming journey of learning.",
            "description": "An eight-year-old boy named Ishaan suffers silently from dyslexia and is misunderstood by his family and school. When an unconventional art teacher Ram Shankar Nikumbh enters his boarding school life, he discovers the boy's magical potential and transforms his world.",
            "genre": "Education, Family Drama, Inspiring",
            "theme_tags": "education, child psychology, dyslexia, teacher, school, inspiring, family, learning, student",
            "language": "Hindi",
            "certification": "U",
            "duration": 165,
            "rating": 9.0,
            "tomatometer": 96,
            "director": "Aamir Khan",
            "cast": "Darsheel Safary, Aamir Khan, Tisca Chopra, Vipin Sharma",
            "music_director": "Shankar-Ehsaan-Loy",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2007, 12, 21),
            "poster": "/static/posters/taare_zameen_par.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Hindi Medium",
            "tagline": "Education is the key, but language is the divide.",
            "description": "A wealthy boutique owner in Old Delhi and his ambitious wife go to extreme, hilarious, and touching lengths including pretending to be poverty-stricken under the RTE quota to get their young daughter admitted into a top elite English-medium private school.",
            "genre": "Education, Satirical Comedy, Social Drama",
            "theme_tags": "education, school admission, satire, comedy, english medium, social drama, parents, student",
            "language": "Hindi",
            "certification": "U",
            "duration": 132,
            "rating": 8.3,
            "tomatometer": 89,
            "director": "Saket Chaudhary",
            "cast": "Irrfan Khan, Saba Qamar, Deepak Dobriyal, Tillotama Shome",
            "music_director": "Sachin-Jigar",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2017, 5, 19),
            "poster": "/static/posters/hindi_medium.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Nil Battey Sannata",
            "tagline": "A dream has no price tag. Can a mother learn math for her child?",
            "description": "A hard-working domestic maid decides to enroll as a 10th-grade high school student in the very same classroom as her unmotivated daughter to challenge her in mathematics and prove that poverty does not dictate one's educational destiny.",
            "genre": "Education, Family Drama, Inspiring",
            "theme_tags": "education, student, mother daughter, maths, 10th class, inspiring, school, study, exam",
            "language": "Hindi",
            "certification": "U",
            "duration": 104,
            "rating": 8.5,
            "tomatometer": 92,
            "director": "Ashwiny Iyer Tiwari",
            "cast": "Swara Bhasker, Riya Shukla, Ratna Pathak Shah, Pankaj Tripathi",
            "music_director": "Rohan & Vinayak",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2016, 4, 22),
            "poster": "/static/posters/nil_battey_sannata.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Chhichhore",
            "tagline": "Winners never quit, and losers are the ones who don't try!",
            "description": "When a student attempts suicide after failing the engineering entrance exam, his divorced parents gather their old college gang of 'Losers' to narrate their unforgettable college hostel days, proving that success in exams does not define the value of life.",
            "genre": "Education, College Comedy, Emotional Drama",
            "theme_tags": "education, college hostel, engineering, student pressure, friendship, sports, nostalgia, exam stress",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 143,
            "rating": 8.6,
            "tomatometer": 93,
            "director": "Nitesh Tiwari",
            "cast": "Sushant Singh Rajput, Shraddha Kapoor, Varun Sharma, Tahir Raj Bhasin",
            "music_director": "Pritam",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2019, 9, 6),
            "poster": "/static/posters/chhichhore.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Hichki",
            "tagline": "There are no bad students, only bad teachers.",
            "description": "Naina Mathur, an aspiring teacher with Tourette Syndrome, lands a job at an elite school assigned to teach Section 9F—a classroom of rebellious, underprivileged students whom society has discarded. She turns their hiccups into superpowers.",
            "genre": "Education, Inspiring Drama, Classroom Mentorship",
            "theme_tags": "education, teacher, tourette syndrome, underprivileged students, classroom, inspiring, school, study",
            "language": "Hindi",
            "certification": "U",
            "duration": 116,
            "rating": 8.2,
            "tomatometer": 87,
            "director": "Siddharth P. Malhotra",
            "cast": "Rani Mukerji, Neeraj Kabi, Rohit Saraf, Supriya Pilgaonkar",
            "music_director": "Jasleen Royal",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2018, 3, 23),
            "poster": "/static/posters/hichki.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "English Vinglish",
            "tagline": "Mind your language, respect your soul.",
            "description": "Shashi, a quiet and sweet-tempered Indian homemaker, is constantly mocked by her educated husband and daughter for her poor English. During a trip to New York, she secretly enrolls in an English-speaking class, rediscovering self-respect.",
            "genre": "Education, Drama, Women Empowerment",
            "theme_tags": "education, learning english, self respect, language class, inspiring, homemaker, student, dignity",
            "language": "Hindi",
            "certification": "U",
            "duration": 134,
            "rating": 8.5,
            "tomatometer": 94,
            "director": "Gauri Shinde",
            "cast": "Sridevi, Adil Hussain, Mehdi Nebbou, Priya Anand",
            "music_director": "Amit Trivedi",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2012, 10, 5),
            "poster": "/static/posters/english_vinglish.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },

        # =========================================================================
        # 2. HORROR COMEDY, SUPERNATURAL & FOLK HORROR (7 Films)
        # =========================================================================
        {
            "title": "Stree 2: Sarkate Ka Aatank",
            "tagline": "O Stree Raksha Karna! The Chanderi saga returns with ultimate horror comedy!",
            "description": "After the events of Stree, the town of Chanderi is haunted by a menacing headless phantom called Sarkata, who preys on modern independent women. Vicky, Bittu, JD, and Rudra must team up with Stree to save their town.",
            "genre": "Horror Comedy, Supernatural, Folklore Masala",
            "theme_tags": "horror, comedy, supernatural, bhoot, chanderi, ghost, sarkata, monster, folklore, terror",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 147,
            "rating": 9.2,
            "tomatometer": 94,
            "director": "Amar Kaushik",
            "cast": "Shraddha Kapoor, Rajkummar Rao, Pankaj Tripathi, Abhishek Banerjee",
            "music_director": "Sachin-Jigar",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2024, 8, 15),
            "poster": "/static/posters/stree_2_sarkate_ka_aatank.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Stree (Part 1)",
            "tagline": "Mard ko dard hoga! The legend of the female phantom in Chanderi.",
            "description": "In the historic town of Chanderi, a female spirit named Stree abducts men at night during annual four-day festival. Vicky, a talented ladies tailor, falls in love with a mysterious girl while trying to solve the supernatural mystery.",
            "genre": "Horror Comedy, Mystery, Folklore",
            "theme_tags": "horror, comedy, ghost, bhoot, chanderi, supernatural, mystery, folklore, fear",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 128,
            "rating": 8.8,
            "tomatometer": 93,
            "director": "Amar Kaushik",
            "cast": "Rajkummar Rao, Shraddha Kapoor, Pankaj Tripathi, Aparshakti Khurana",
            "music_director": "Sachin-Jigar",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2018, 8, 31),
            "poster": "/static/posters/stree_part_1.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Bhool Bhulaiyaa 3",
            "tagline": "Rooh Baba returns to face the wrath of the royal spirit!",
            "description": "Ruhaan, also known as Rooh Baba, is hired by a royal family in Bengal to exorcise a cursed palace, only to discover that the terrifying spirit of Manjulika has returned with double the vengeance.",
            "genre": "Horror Comedy, Mystery, Masala Thriller",
            "theme_tags": "horror, comedy, manjulika, ghost, palace, rooh baba, mystery, supernatural, bhoot",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 158,
            "rating": 7.8,
            "tomatometer": 82,
            "director": "Anees Bazmee",
            "cast": "Kartik Aaryan, Vidya Balan, Madhuri Dixit, Triptii Dimri",
            "music_director": "Pritam, Tanishk Bagchi",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2024, 11, 1),
            "poster": "/static/posters/bhool_bhulaiyaa_3.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Bhool Bhulaiyaa 2",
            "tagline": "Dhavak mahal mein Rooh Baba aur Manjulika ki aamne saamne takkar!",
            "description": "Ruhaan and Reet pose as a couple and take shelter in a supposedly haunted ancestral mansion in Rajasthan, accidentally releasing the trapped malevolent spirit of Manjulika after 18 years.",
            "genre": "Horror Comedy, Supernatural, Mystery",
            "theme_tags": "horror, comedy, ghost, manjulika, spirit, haveli, rooh baba, supernatural, bhoot",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 143,
            "rating": 8.1,
            "tomatometer": 86,
            "director": "Anees Bazmee",
            "cast": "Kartik Aaryan, Tabu, Kiara Advani, Rajpal Yadav",
            "music_director": "Pritam, Tanishk Bagchi",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2022, 5, 20),
            "poster": "/static/posters/bhool_bhulaiyaa_2.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Tumbbad (4K Remastered)",
            "tagline": "Greed has no end. The legend of Hastar reborn in 4K Atmos.",
            "description": "In 1918 Maharashtra, Vinayak Rao seeks a legendary cursed ancestral treasure belonging to Hastar, the demon god of greed. A masterclass in Indian period atmospheric horror and human avarice.",
            "genre": "Horror, Period Fantasy, Mythological Folk Horror",
            "theme_tags": "horror, hastar, period fantasy, greed, curse, demon, mythological, folk horror, supernatural",
            "language": "Hindi",
            "certification": "A",
            "duration": 104,
            "rating": 8.9,
            "tomatometer": 95,
            "director": "Rahi Anil Barve",
            "cast": "Sohum Shah, Jyoti Malshe, Anita Date, Deepak Damle",
            "music_director": "Jesper Kyd, Ajay-Atul",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2018, 10, 12),
            "poster": "/static/posters/tumbbad_4k_remastered.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Munjya",
            "tagline": "The Kokan folklore spirit seeking his true bride!",
            "description": "Bittu accidentally awakens the restless and mischievous spirit of Munjya—a young boy from 1952 cursed to wander a haunted peepal tree in coastal Maharashtra. A thrilling folk horror comedy blend.",
            "genre": "Horror Comedy, Folk Legend, Supernatural",
            "theme_tags": "horror, comedy, folklore, kokan, spirit, supernatural, monster, munjya, ghost, bhoot",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 123,
            "rating": 8.1,
            "tomatometer": 88,
            "director": "Aditya Sarpotdar",
            "cast": "Abhay Verma, Sharvari Wagh, Mona Singh, Sathyaraj",
            "music_director": "Sachin-Jigar",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2024, 6, 7),
            "poster": "/static/posters/munjya.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Bhediya",
            "tagline": "Jungle mein kaand ho gaya! The creature comedy universe.",
            "description": "Bhaskar, a road contractor in the forests of Ziro, Arunachal Pradesh, is bitten by a mythical shape-shifting golden wolf. Soon, he starts transforming into a werewolf every full moon night to protect the ecology.",
            "genre": "Horror Comedy, Creature Feature, Fantasy",
            "theme_tags": "horror, comedy, werewolf, jungle, arunachal, supernatural, shapeshifter, monster, bhoot",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 156,
            "rating": 7.9,
            "tomatometer": 85,
            "director": "Amar Kaushik",
            "cast": "Varun Dhawan, Kriti Sanon, Abhishek Banerjee, Deepak Dobriyal",
            "music_director": "Sachin-Jigar",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2022, 11, 25),
            "poster": "/static/posters/bhediya.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },

        # =========================================================================
        # 3. ACTION, UNDERWORLD CRIME, GANGSTER & COP MASALA (8 Films)
        # =========================================================================
        {
            "title": "Animal",
            "tagline": "A son's primal obsession and unhinged loyalty.",
            "description": "A son's love for his distant industrialist father crosses extreme boundaries, spiraling into a brutal saga of underworld vengeance, high stakes, and psychological transformation.",
            "genre": "Action, Crime Drama, Underworld Syndicate",
            "theme_tags": "crime, mafia, underworld, violence, father son, vengeance, action, syndicate, dark thriller, shootout",
            "language": "Hindi",
            "certification": "A",
            "duration": 204,
            "rating": 8.8,
            "tomatometer": 89,
            "director": "Sandeep Reddy Vanga",
            "cast": "Ranbir Kapoor, Anil Kapoor, Bobby Deol, Rashmika Mandanna",
            "music_director": "Harshavardhan Rameshwar & JAM8",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2023, 12, 1),
            "poster": "/static/posters/animal.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "K.G.F: Chapter 2",
            "tagline": "Violence violence violence! I don't like it, but violence likes me!",
            "description": "The blood-soaked land of Kolar Gold Fields has a new overlord: Rocky. While his allies look up to him, the government and bloodthirsty rivals like Adheera and Inayat Khalil see him as the ultimate threat.",
            "genre": "Action, Period Crime, Mass Masala",
            "theme_tags": "crime, mafia, gold fields, underworld, rocky bhai, mass action, empire, violence, shootout",
            "language": "Kannada",
            "certification": "U/A",
            "duration": 168,
            "rating": 8.7,
            "tomatometer": 92,
            "director": "Prashanth Neel",
            "cast": "Yash, Sanjay Dutt, Raveena Tandon, Srinidhi Shetty",
            "music_director": "Ravi Basrur",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2022, 4, 14),
            "poster": "/static/posters/kgf_chapter_2.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Salaar: Part 1 – Ceasefire",
            "tagline": "The violent bond of blood and power in the dystopian city of Khansaar.",
            "description": "In the cutthroat dystopian city-state of Khansaar, two childhood best friends Deva and Varadha turn from soulmates into warlord rivals during a bloody coup for supremacy.",
            "genre": "Action, Crime Thriller, Warlord Epic",
            "theme_tags": "crime, warlord, khansaar, dystopian, action, blood brothers, coup, violence, syndicate",
            "language": "Telugu",
            "certification": "A",
            "duration": 175,
            "rating": 8.2,
            "tomatometer": 85,
            "director": "Prashanth Neel",
            "cast": "Prabhas, Prithviraj Sukumaran, Shruti Haasan, Jagapathi Babu",
            "music_director": "Ravi Basrur",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2023, 12, 22),
            "poster": "/static/posters/salaar_part_1__ceasefire.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Pushpa 2: The Rule",
            "tagline": "Pushpa jhukega nahi! The Red Sandalwood Emperor strikes back!",
            "description": "Pushpa Raj expands his red sandalwood smuggling empire across international waters, engaging in high-stakes warfare with police SP Bhanwar Singh Shekhawat and rival cartel syndicates.",
            "genre": "Action Masala, Crime Syndicate, Pan-Indian Thriller",
            "theme_tags": "crime, syndicate, red sandalwood, smuggling, mass action, police clash, emperor, cartel",
            "language": "Telugu",
            "certification": "U/A",
            "duration": 190,
            "rating": 9.0,
            "tomatometer": 91,
            "director": "Sukumar",
            "cast": "Allu Arjun, Rashmika Mandanna, Fahadh Faasil, Jagadeesh Prathap",
            "music_director": "Devi Sri Prasad (DSP)",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2024, 12, 5),
            "poster": "/static/posters/pushpa_2_the_rule.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Vikram",
            "tagline": "Once upon a time there lived a ghost... Inception of the LCU narcotics war!",
            "description": "A special investigation team officer probes a masked gang of vigilantes executing corrupt police officials, leading to a massive clash with a deadly narcotics kingpin Sandhanam and the legendary black-ops operative Agent Vikram.",
            "genre": "Action, Crime Neo-Noir, Narcotics Underworld",
            "theme_tags": "crime, narcotics, cartel, police, black ops, agent vikram, rolex, action, shootout, mafia",
            "language": "Tamil",
            "certification": "U/A",
            "duration": 174,
            "rating": 8.8,
            "tomatometer": 94,
            "director": "Lokesh Kanagaraj",
            "cast": "Kamal Haasan, Fahadh Faasil, Vijay Sethupathi, Suriya",
            "music_director": "Anirudh Ravichander",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2022, 6, 3),
            "poster": "/static/posters/vikram.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Gangs of Wasseypur",
            "tagline": "Baap ka, dada ka, bhai ka; sabka badla lega re tera Faizal!",
            "description": "A clash between Sultan and Shahid Khan leads to the expulsion of Khan from Wasseypur, sparking a deadly three-generation blood feud between powerful coal mafia families in Dhanbad.",
            "genre": "Crime, Gangster Epic, Dark Comedy",
            "theme_tags": "crime, mafia, coal mafia, gangster, revenge, dhanbad, shootout, blood feud, violence, underworld",
            "language": "Hindi",
            "certification": "A",
            "duration": 320,
            "rating": 9.1,
            "tomatometer": 96,
            "director": "Anurag Kashyap",
            "cast": "Manoj Bajpayee, Nawazuddin Siddiqui, Richa Chadha, Tigmanshu Dhulia, Pankaj Tripathi",
            "music_director": "Sneha Khanwalkar",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2012, 6, 22),
            "poster": "/static/posters/gangs_of_wasseypur.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Drishyam 2",
            "tagline": "Can confessions be crafted? The Salgaonkar family suspense saga.",
            "description": "Seven years after the case was buried, IG Tarun Ahlawat reopens the disappearance of Sameer Deshmukh. Vijay Salgaonkar must use his sharp cinematic intellect and forensic genius once again to shield his family.",
            "genre": "Crime, Suspense Mystery, Courtroom Thriller",
            "theme_tags": "crime, police investigation, murder mystery, courtroom, family suspense, alibi, thriller",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 140,
            "rating": 8.6,
            "tomatometer": 91,
            "director": "Abhishek Pathak",
            "cast": "Ajay Devgn, Tabu, Akshaye Khanna, Shriya Saran",
            "music_director": "Devi Sri Prasad",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2022, 11, 18),
            "poster": "/static/posters/drishyam_2.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Jawan",
            "tagline": "Ready Chief? A high-octane emotional action thriller!",
            "description": "A man is driven by a personal vendetta to rectify the wrongs in society, while keeping a promise made years ago. He comes up against a monstrous outlaw who knows no fear and has caused extreme suffering to many.",
            "genre": "Action, Masala Thriller, Vigilante Crime Drama",
            "theme_tags": "action, vigilante, crime, corruption, father son, army, social justice, mass masala, shootout",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 169,
            "rating": 9.1,
            "tomatometer": 93,
            "director": "Atlee Kumar",
            "cast": "Shah Rukh Khan, Nayanthara, Vijay Sethupathi, Deepika Padukone",
            "music_director": "Anirudh Ravichander",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2023, 9, 7),
            "poster": "/static/posters/jawan.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },

        # =========================================================================
        # 4. PATRIOTISM, ARMED FORCES & MILITARY ACTION (5 Films)
        # =========================================================================
        {
            "title": "Fighter",
            "tagline": "Air Dragons of India: Airborne courage and ultimate sacrifice.",
            "description": "Top Indian Air Force fighter aviators unite under the 'Air Dragons' unit to defend the skies and retaliate against cross-border terror threats in Jammu and Kashmir, navigating high-g dogfights and personal loss.",
            "genre": "Action, Patriotism, Aerial Military Thriller",
            "theme_tags": "patriotism, air force, fighter pilots, defense, armed forces, war, aerial action, sacrifice, nation, military",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 166,
            "rating": 8.1,
            "tomatometer": 86,
            "director": "Siddharth Anand",
            "cast": "Hrithik Roshan, Deepika Padukone, Anil Kapoor, Karan Singh Grover",
            "music_director": "Vishal-Shekhar",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2024, 1, 25),
            "poster": "/static/posters/fighter.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Uri: The Surgical Strike",
            "tagline": "How's the Josh? High, Sir! The true story of the 2016 surgical strike.",
            "description": "Major Vihaan Singh Shergill of the Indian Para Special Forces leads a covert counter-terrorist retaliation strike across the border in Pakistan-occupied Kashmir following the tragic Uri terror attack.",
            "genre": "Action, Military Drama, Patriotism",
            "theme_tags": "patriotism, indian army, surgical strike, special forces, kashmir, military, retaliation, nation, soldier",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 138,
            "rating": 8.9,
            "tomatometer": 94,
            "director": "Aditya Dhar",
            "cast": "Vicky Kaushal, Yami Gautam, Paresh Rawal, Mohit Raina",
            "music_director": "Shashwat Sachdev",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2019, 1, 11),
            "poster": "/static/posters/uri_the_surgical_strike.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Shershaah",
            "tagline": "Yeh Dil Maange More! The immortal valor of Captain Vikram Batra PVC.",
            "description": "The heroic life and supreme sacrifice of Param Vir Chakra awardee Captain Vikram Batra during the 1999 Kargil War, capturing Point 5140 and Point 4875 against intense enemy artillery.",
            "genre": "Patriotism, War Biopic, Romance",
            "theme_tags": "patriotism, kargil war, param vir chakra, indian army, captain vikram batra, soldier, sacrifice, nation",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 135,
            "rating": 8.8,
            "tomatometer": 93,
            "director": "Vishnuvardhan",
            "cast": "Sidharth Malhotra, Kiara Advani, Shiv Panditt, Nikitin Dheer",
            "music_director": "Tanishk Bagchi & Jasleen Royal",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2021, 8, 12),
            "poster": "/static/posters/shershaah.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Border",
            "tagline": "The legendary stand of 120 soldiers at the Battle of Longewala.",
            "description": "During the Indo-Pakistani War of 1971, a small battalion of 120 Indian Army soldiers at Longewala post valiantly holds off an entire enemy armoured tank brigade throughout the night until IAF Hawker Hunters arrive.",
            "genre": "War, Patriotism, Cult Classic",
            "theme_tags": "patriotism, longewala, 1971 war, indian army, soldier, brotherhood, sacrifice, classic, military",
            "language": "Hindi",
            "certification": "U",
            "duration": 178,
            "rating": 8.7,
            "tomatometer": 92,
            "director": "J. P. Dutta",
            "cast": "Sunny Deol, Suniel Shetty, Akshaye Khanna, Jackie Shroff, Puneet Issar",
            "music_director": "Anu Malik",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(1997, 6, 13),
            "poster": "/static/posters/border.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Pathaan",
            "tagline": "Apni kursi ki peti baandh lo, mausam bigadne wala hai!",
            "description": "An exiled RAW field operative returns to stop Outfit X, a rogue mercenary army led by Jim, from unleashing a deadly viral biological weapon across Indian metropolitan centers.",
            "genre": "Action, Spy Thriller, Patriotic Espionage",
            "theme_tags": "patriotism, raw agent, spy, espionage, biological weapon, action thriller, nation, military",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 146,
            "rating": 8.5,
            "tomatometer": 88,
            "director": "Siddharth Anand",
            "cast": "Shah Rukh Khan, Deepika Padukone, John Abraham, Dimple Kapadia",
            "music_director": "Vishal-Shekhar",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2023, 1, 25),
            "poster": "/static/posters/pathaan.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },

        # =========================================================================
        # 5. MYTHOLOGY, SCI-FI & HISTORICAL EPICS (6 Films)
        # =========================================================================
        {
            "title": "Kalki 2898 AD",
            "tagline": "The future of humanity meets the prophecy of Mahabharata.",
            "description": "Set in a dystopian post-apocalyptic Kashi in the year 2898 AD, bounty hunter Bhairava crosses paths with immortal Ashwatthama to protect SUM-80 and the unborn tenth avatar of Lord Vishnu from the tyrannical Supreme Yaskin.",
            "genre": "Mythology, Sci-Fi, Dystopian Epic, Astraverse",
            "theme_tags": "mythology, mahabharata, sci-fi, dystopia, ashwatthama, kalki avatar, god, futuristic, epic",
            "language": "Telugu",
            "certification": "U/A",
            "duration": 181,
            "rating": 8.9,
            "tomatometer": 90,
            "director": "Nag Ashwin",
            "cast": "Prabhas, Amitabh Bachchan, Kamal Haasan, Deepika Padukone",
            "music_director": "Santhosh Narayanan",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2024, 6, 27),
            "poster": "/static/posters/kalki_2898_ad.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "RRR (Rise Roar Revolt)",
            "tagline": "Fire and Water unite to ignite the revolution of a nation!",
            "description": "A fearless revolutionary Komaram Bheem and an iron-willed British cop Alluri Sitarama Raju form an unbreakable brotherly bond without knowing each other's secret identities, setting off an explosive war against the British Raj.",
            "genre": "Historical Epic, Action Drama, Revolution Masala",
            "theme_tags": "mythology, historical epic, revolution, rebellion, friendship, ramaraju, bheem, action, folklore",
            "language": "Telugu",
            "certification": "U/A",
            "duration": 187,
            "rating": 9.3,
            "tomatometer": 96,
            "director": "S. S. Rajamouli",
            "cast": "N. T. Rama Rao Jr., Ram Charan, Alia Bhatt, Ajay Devgn",
            "music_director": "M. M. Keeravani",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2022, 3, 25),
            "poster": "/static/posters/rrr_rise_roar_revolt.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Kantara",
            "tagline": "A mystical tale of divine folklore, man vs nature, and Daiva justice.",
            "description": "In a coastal Karnataka village bordering lush sacred forests, a rebellious kambala bull race champion Shiva clashes with an unyielding forest officer Murali, igniting the divine ancestral wrath of Panjurli and Guliga Daiva.",
            "genre": "Mythology, Folklore Action, Spiritual Tribal Epic",
            "theme_tags": "mythology, panjurli daiva, guliga, divine spirit, folklore, forest, tribal, spiritual, god",
            "language": "Kannada",
            "certification": "U/A",
            "duration": 148,
            "rating": 9.1,
            "tomatometer": 95,
            "director": "Rishab Shetty",
            "cast": "Rishab Shetty, Sapthami Gowda, Kishore, Achyuth Kumar",
            "music_director": "B. Ajaneesh Loknath",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2022, 9, 30),
            "poster": "/static/posters/kantara.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Baahubali 2: The Conclusion",
            "tagline": "Why did Katappa kill Baahubali? The answer that shook Indian cinema.",
            "description": "When Amarendra Baahubali is proclaimed the rightful ruler of Mahishmati kingdom, the jealous Bhallaladeva conspires with Bijjaladeva to turn Queen Sivagami against him, culminating in the ultimate royal sacrifice.",
            "genre": "Mythology, Historical Epic, Royal Action Fantasy",
            "theme_tags": "mythology, mahishmati, royal epic, king, katappa, amarendra baahubali, historical fantasy, god",
            "language": "Telugu",
            "certification": "U/A",
            "duration": 167,
            "rating": 9.2,
            "tomatometer": 95,
            "director": "S. S. Rajamouli",
            "cast": "Prabhas, Rana Daggubati, Anushka Shetty, Ramya Krishna, Sathyaraj",
            "music_director": "M. M. Keeravani",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2017, 4, 28),
            "poster": "/static/posters/baahubali_2_the_conclusion.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Brahmāstra: Part One – Shiva",
            "tagline": "The Astraverse awakens. Love is the greatest weapon.",
            "description": "Shiva, a Mumbai DJ with an innate mystical immunity to fire, discovers that he is the Agnyastra herself. Guided by Guru Arvind, he must protect the Brahmashira from the dark queen Junoon.",
            "genre": "Fantasy, Mythology, Superhero Astraverse",
            "theme_tags": "mythology, astraverse, agnyastra, superpowers, brahmashira, romance, fantasy, god",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 167,
            "rating": 7.9,
            "tomatometer": 84,
            "director": "Ayan Mukerji",
            "cast": "Ranbir Kapoor, Alia Bhatt, Amitabh Bachchan, Nagarjuna, Mouni Roy",
            "music_director": "Pritam",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2022, 9, 9),
            "poster": "/static/posters/brahmāstra_part_one__shiva.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Hanu-Man",
            "tagline": "An ancient divine power bestowed upon a simple village thief.",
            "description": "In the fictional village of Anjanadri, Hanumanthu discovers a mythical solar gem holding the boundless celestial power of Lord Hanuman, rising to defend his people from a megalomaniac tech villain.",
            "genre": "Mythology, Superhero, Fantasy Action",
            "theme_tags": "mythology, lord hanuman, superhero, divine gem, village, fantasy, epic, god, astraverse",
            "language": "Telugu",
            "certification": "U/A",
            "duration": 158,
            "rating": 8.3,
            "tomatometer": 89,
            "director": "Prasanth Varma",
            "cast": "Teja Sajja, Amritha Aiyer, Varalaxmi Sarathkumar, Vinay Rai",
            "music_director": "Anudeep Dev",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2024, 1, 12),
            "poster": "/static/posters/hanu-man.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },

        # =========================================================================
        # 6. SPORTS, INSPIRING BIOPICS & SURVIVAL DRAMAS (5 Films)
        # =========================================================================
        {
            "title": "Dangal",
            "tagline": "Mhaari chhoriyan chhoron se kam hain ke? The wrestling revolution.",
            "description": "Former amateur wrestling champion Mahavir Singh Phogat trains his young daughters Geeta and Babita in rural Haryana, battling deeply ingrained societal patriarchy to coach them to Commonwealth Games gold medals.",
            "genre": "Sports, Biographical Drama, Wrestling",
            "theme_tags": "sports, wrestling, commonwealth gold, father daughters, haryana, biopic, inspiring, coaching",
            "language": "Hindi",
            "certification": "U",
            "duration": 161,
            "rating": 9.2,
            "tomatometer": 98,
            "director": "Nitesh Tiwari",
            "cast": "Aamir Khan, Fatima Sana Shaikh, Sanya Malhotra, Sakshi Tanwar",
            "music_director": "Pritam",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2016, 12, 23),
            "poster": "/static/posters/dangal.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Chak De! India",
            "tagline": "Sattar Minute! The underdog Indian Women's Hockey Team saga.",
            "description": "Disgraced former Indian men's hockey captain Kabir Khan takes up the challenge of coaching a fractured, neglected Indian National Women's Hockey Team, transforming 16 regional rival players into World Champions.",
            "genre": "Sports, Patriotic Drama, Teamwork",
            "theme_tags": "sports, women hockey team, world cup, coach, patriotism, underdog, inspiring, teamwork",
            "language": "Hindi",
            "certification": "U",
            "duration": 153,
            "rating": 8.9,
            "tomatometer": 95,
            "director": "Shimit Amin",
            "cast": "Shah Rukh Khan, Vidya Malvade, Sagarika Ghatge, Shilpa Shukla",
            "music_director": "Salim-Sulaiman",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2007, 8, 10),
            "poster": "/static/posters/chak_de_india.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Bhaag Milkha Bhaag",
            "tagline": "The true story of the Flying Sikh who outran his deepest trauma.",
            "description": "The biographical journey of Milkha Singh, an Indian athlete who overcame the horrific trauma of the 1947 Partition massacre, juvenile crime, and army discipline to become an Olympic champion and national icon.",
            "genre": "Sports, Biographical Drama, Athletics",
            "theme_tags": "sports, flying sikh, athletics, race, gold medal, partition, biopic, inspiring, olympics",
            "language": "Hindi",
            "certification": "U",
            "duration": 186,
            "rating": 8.8,
            "tomatometer": 92,
            "director": "Rakeysh Omprakash Mehra",
            "cast": "Farhan Akhtar, Sonam Kapoor, Divya Dutta, Pavan Malhotra",
            "music_director": "Shankar-Ehsaan-Loy",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2013, 7, 12),
            "poster": "/static/posters/bhaag_milkha_bhaag.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "MS Dhoni: The Untold Story",
            "tagline": "The journey of a ticket collector who lifted the 2011 Cricket World Cup.",
            "description": "The inspiring life of Mahendra Singh Dhoni, from a small-town railway ticket examiner in Kharagpur with unfulfilled cricketing dreams to leading Team India to triumph in the 2011 ICC Cricket World Cup.",
            "genre": "Sports, Cricket Biopic, Inspiring",
            "theme_tags": "sports, cricket, captain cool, world cup, ticket collector, biopic, inspiring, coaching",
            "language": "Hindi",
            "certification": "U",
            "duration": 184,
            "rating": 8.7,
            "tomatometer": 91,
            "director": "Neeraj Pandey",
            "cast": "Sushant Singh Rajput, Kiara Advani, Disha Patani, Anupam Kher",
            "music_director": "Amaal Mallik & Rochak Kohli",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2016, 9, 30),
            "poster": "/static/posters/ms_dhoni_the_untold_story.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Manjummel Boys",
            "tagline": "Human bonds deeper than the deepest abyss. Based on Guna Caves rescue.",
            "description": "A close-knit group of carefree friends from Kochi travel on a holiday trip to Kodaikanal, where one of them accidentally plunges into the bottomless subterranean Devil's Kitchen Guna Cave. Defying all odds and police refusal, his friends attempt the impossible rescue.",
            "genre": "Survival, Adventure Drama, True Friendship",
            "theme_tags": "sports, survival, guna caves, friendship, kodaikanal, rescue, true story, adventure, inspiring",
            "language": "Malayalam",
            "certification": "U",
            "duration": 135,
            "rating": 9.0,
            "tomatometer": 97,
            "director": "Chidambaram",
            "cast": "Soubin Shahir, Sreenath Bhasi, Balu Varghese, Ganapathi",
            "music_director": "Sushin Shyam",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2024, 2, 22),
            "poster": "/static/posters/manjummel_boys.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },

        # =========================================================================
        # 7. ROMANCE, SOULFUL MUSICALS & ALL-TIME CLASSICS (7 Films)
        # =========================================================================
        {
            "title": "Dilwale Dulhania Le Jayenge",
            "tagline": "Come... fall in love. The definitive Bollywood romance.",
            "description": "Raj and Simran fall deeply in love on a Eurail train journey through Switzerland. Raj follows Simran all the way to mustard fields of Punjab to win the blessing of her traditional father Chaudhry Baldev Singh without eloping.",
            "genre": "Romance, Musical, Family Drama, Classic",
            "theme_tags": "romance, ddlj, raj simran, punjab, mustard fields, wedding, classic, musical, love",
            "language": "Hindi",
            "certification": "U",
            "duration": 189,
            "rating": 9.3,
            "tomatometer": 96,
            "director": "Aditya Chopra",
            "cast": "Shah Rukh Khan, Kajol, Amrish Puri, Anupam Kher, Farida Jalal",
            "music_director": "Jatin-Lalit",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(1995, 10, 20),
            "poster": "/static/posters/dilwale_dulhania_le_jayenge.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Jab We Met",
            "tagline": "Main apni favorite hoon! The train ride that healed a broken heart.",
            "description": "A depressed, suicidal Mumbai business tycoon Aditya meets Geet, a vivacious and carefree Punjabi girl on a late-night train. She drags him on a whirlwind journey across Ratlam and Bhatinda, fundamentally changing his perspective on life and love.",
            "genre": "Romance, Romantic Comedy, Musical",
            "theme_tags": "romance, geet aditya, train journey, bhatinda, heartbreak, feel good, musical, classic, love",
            "language": "Hindi",
            "certification": "U",
            "duration": 142,
            "rating": 8.9,
            "tomatometer": 95,
            "director": "Imtiaz Ali",
            "cast": "Shahid Kapoor, Kareena Kapoor Khan, Tarun Arora, Saumya Tandon",
            "music_director": "Pritam & Sandesh Shandilya",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2007, 10, 26),
            "poster": "/static/posters/jab_we_met.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Yeh Jawaani Hai Deewani",
            "tagline": "Kahin pahunchne ke liye kahin se nikalna zaroori hota hai!",
            "description": "Bunny, an ambitious free-spirited photographer who wants to see the world, and Naina, a studious medical scholar, bond on a trekking trip to Manali and reunite eight years later at a friend's lavish destination wedding in Udaipur.",
            "genre": "Romance, Coming-of-Age, Musical",
            "theme_tags": "romance, bunny naina, travel, friendship, wedding, wanderlust, youth, musical, love",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 160,
            "rating": 8.6,
            "tomatometer": 92,
            "director": "Ayan Mukerji",
            "cast": "Ranbir Kapoor, Deepika Padukone, Aditya Roy Kapur, Kalki Koechlin",
            "music_director": "Pritam",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2013, 5, 31),
            "poster": "/static/posters/yeh_jawaani_hai_deewani.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Aashiqui 2",
            "tagline": "Love that makes you immortal. The definitive musical tragedy.",
            "description": "Rahul Jaykar, a fading alcoholic music star, discovers Aarohi singing in a small Goa bar. He mentors her to become a national playback sensation, but his own self-destructive demons threaten their tragic love.",
            "genre": "Romance, Musical Tragedy, Drama",
            "theme_tags": "romance, rahul aarohi, singing, tragedy, love, heartbreak, soulful musical, alcohol",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 132,
            "rating": 8.3,
            "tomatometer": 88,
            "director": "Mohit Suri",
            "cast": "Aditya Roy Kapur, Shraddha Kapoor, Shaad Randhawa, Mahesh Thakur",
            "music_director": "Mithoon, Ankit Tiwari, Jeet Gannguli",
            "is_trending": False,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2013, 4, 26),
            "poster": "/static/posters/aashiqui_2.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Bajrangi Bhaijaan",
            "tagline": "A journey of pure heart, humanity, and boundless love across borders.",
            "description": "Pawan Kumar Chaturvedi, a devoted Hanuman bhakt, meets a mute 6-year-old Pakistani girl stranded in India. Against intense geopolitical hostility, he embarks on an emotional cross-border odyssey to reunite her with her mother.",
            "genre": "Drama, Comedy, Human Emotion",
            "theme_tags": "romance, drama, humanity, border crossing, munni, pawan, love, feel good, family",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 159,
            "rating": 9.0,
            "tomatometer": 95,
            "director": "Kabir Khan",
            "cast": "Salman Khan, Harshaali Malhotra, Kareena Kapoor Khan, Nawazuddin Siddiqui",
            "music_director": "Pritam",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2015, 7, 17),
            "poster": "/static/posters/bajrangi_bhaijaan.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/fVV0A67kDjTTQ4CvUn8LoletRmI.jpg"
        },
        {
            "title": "Sholay (4K Remastered)",
            "tagline": "Yeh Haath Humko De De Thakur! India's greatest curry western classic.",
            "description": "Retired police officer Thakur Baldev Singh hires two fearless ex-convict rogues Jai and Veeru in the rugged ravines of Ramgarh to capture the ruthless dacoit chieftain Gabbar Singh alive.",
            "genre": "Action, Curry Western, Cult Classic",
            "theme_tags": "classic, jai veeru, gabbar singh, thakur, ramgarh, curry western, action, all-time blockbuster, romance",
            "language": "Hindi",
            "certification": "U",
            "duration": 198,
            "rating": 9.4,
            "tomatometer": 99,
            "director": "Ramesh Sippy",
            "cast": "Amitabh Bachchan, Dharmendra, Sanjeev Kumar, Hema Malini, Amjad Khan",
            "music_director": "R. D. Burman",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(1975, 8, 15),
            "poster": "/static/posters/sholay_4k_remastered.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        },
        {
            "title": "Zindagi Na Milegi Dobara",
            "tagline": "Seize the day, overcome your deepest fears.",
            "description": "Three childhood friends Kabir, Imran, and Arjun embark on an ultimate bachelor road trip across Spain, confronting their past regrets, phobias through extreme sports (deep-sea diving, skydiving, running of bulls), and redefining happiness.",
            "genre": "Drama, Comedy, Friendship Adventure",
            "theme_tags": "romance, friendship, road trip, spain, diving, skydiving, feel good, coming-of-age, classic, love",
            "language": "Hindi",
            "certification": "U/A",
            "duration": 155,
            "rating": 8.9,
            "tomatometer": 94,
            "director": "Zoya Akhtar",
            "cast": "Hrithik Roshan, Farhan Akhtar, Abhay Deol, Katrina Kaif, Kalki Koechlin",
            "music_director": "Shankar-Ehsaan-Loy",
            "is_trending": True,
            "is_now_showing": True,
            "is_bollywood_hit": True,
            "release_date": date(2011, 7, 15),
            "poster": "/static/posters/zindagi_na_milegi_dobara.jpg",
            "backdrop": "https://image.tmdb.org/t/p/w1280/5LtSjMNw6j3LkG29Oa4O0iY5U8.jpg"
        }
    ]

    created_movies = []
    for mdata in movies_data:
        m, created = Movie.objects.update_or_create(
            title=mdata["title"],
            defaults=mdata
        )
        created_movies.append(m)

    print(f"✅ Created/Updated {len(created_movies)} Indian Blockbusters with UNIQUE Official Posters in DB.")

    # 3. Multiplex Theaters Across Metros
    theaters_data = [
        {"name": "PVR INOX Palladium", "city": "Mumbai", "address": "High Street Phoenix, Lower Parel, Mumbai", "brand": "PVR INOX"},
        {"name": "Cinépolis Vegas Mall", "city": "Delhi-NCR", "address": "Sector 14, Dwarka, New Delhi", "brand": "Cinepolis"},
        {"name": "PVR Forum Mall", "city": "Bengaluru", "address": "Koramangala 7th Block, Hosur Road, Bengaluru", "brand": "PVR INOX"},
        {"name": "Prasads Multiplex (IMAX)", "city": "Hyderabad", "address": "NTR Gardens, Khairatabad, Hyderabad", "brand": "PVR INOX"},
    ]

    theaters = []
    for tdata in theaters_data:
        th, _ = Theater.objects.get_or_create(
            name=tdata["name"],
            defaults={"city": tdata["city"], "address": tdata["address"], "brand": tdata["brand"]}
        )
        theaters.append(th)

    # 4. Screens & Seats
    screens = []
    for th in theaters:
        for s_idx, s_type in enumerate(["IMAX 3D", "Dolby Atmos 4K"]):
            scr_name = f"Screen {s_idx + 1} - {s_type}"
            scr, _ = Screen.objects.get_or_create(
                theater=th,
                screen_name=scr_name,
                defaults={"screen_type": s_type, "total_rows": 8, "total_cols": 12}
            )
            screens.append(scr)

            if Seat.objects.filter(screen=scr).count() == 0:
                seats = []
                for num in range(1, 7):
                    seats.append(Seat(screen=scr, row_label='A', seat_number=num, seat_type='RECLINER'))
                for row in ['B', 'C', 'D']:
                    for num in range(1, 11):
                        seats.append(Seat(screen=scr, row_label=row, seat_number=num, seat_type='GOLD'))
                for row in ['E', 'F']:
                    for num in range(1, 13):
                        seats.append(Seat(screen=scr, row_label=row, seat_number=num, seat_type='SILVER'))
                Seat.objects.bulk_create(seats)

    # 5. Showtimes for All Movies Across Theaters
    show_times_slots = [time(10, 30), time(14, 0), time(17, 30), time(21, 15)]
    formats = ["IMAX 3D", "Dolby Atmos 4K", "Laser 2D", "INSIGNIA Recliner"]

    today = date.today()
    for m_idx, m in enumerate(created_movies):
        scr = screens[m_idx % len(screens)]
        for day_offset in range(3):
            show_date = today + timedelta(days=day_offset)
            slot = show_times_slots[(m_idx + day_offset) % len(show_times_slots)]
            fmt = formats[(m_idx + day_offset) % len(formats)]
            Showtime.objects.get_or_create(
                movie=m,
                screen=scr,
                show_date=show_date,
                show_time=slot,
                defaults={
                    "silver_price": 240.00,
                    "gold_price": 390.00,
                    "recliner_price": 690.00,
                    "format": fmt,
                    "language": m.language
                }
            )

    # 6. Authentic Indian Cinema Snacks
    snacks_data = [
        {"name": "Dilli 6 Crispy Samosa (2 Pcs)", "category": "SNACKS", "price": 140.00, "description": "Piping hot spiced potato samosas served with sweet saunth and zesty mint chutney."},
        {"name": "Cutting Masala Chai in Clay Kulhad", "category": "BEVERAGES", "price": 90.00, "description": "Slow-brewed aromatic Indian tea with ginger, cardamom, and whole milk."},
        {"name": "Butter Caramel Popcorn (Large Tub)", "category": "POPCORN", "price": 340.00, "description": "Crunchy jumbo corn coated with warm rich golden butter caramel."},
        {"name": "Mumbai Vada Pav Canteen Combo", "category": "SNACKS", "price": 160.00, "description": "2 authentic Batata Vadas in fresh pav with fried green chillies and garlic thecha."},
        {"name": "Nachos with Warm Desi Cheese Dip", "category": "SNACKS", "price": 280.00, "description": "Crisp corn tortilla chips paired with spicy jalapeño melted cheese."},
        {"name": "Masala Thums Up / Cold Coffee", "category": "BEVERAGES", "price": 120.00, "description": "Toofani Thums Up spiced with black salt and cumin / chilled creamy cold coffee."}
    ]

    for sdata in snacks_data:
        SnackItem.objects.update_or_create(name=sdata["name"], defaults=sdata)

    print("🍿 Seeded Desi Canteen Snack Menu.")

    # 7. Sample Reviews
    reviews_data = [
        {"movie": created_movies[0], "user": rahul, "rating": 5, "comment": "12th Fail made me cry and gave immense courage! Vikrant Massey's restart dialogue gave pure goosebumps. Best movie on education ever made!"},
        {"movie": created_movies[1], "user": priya, "rating": 5, "comment": "3 Idiots remains the golden standard for Indian education and engineering college memories. Rancho's philosophy is timeless!"},
        {"movie": created_movies[9], "user": rahul, "rating": 5, "comment": "Stree 2 had the entire theater roaring with laughter and shrieking in terror! Amar Kaushik did it again!"},
    ]

    for rdata in reviews_data:
        Review.objects.get_or_create(movie=rdata["movie"], user=rdata["user"], defaults={"rating": rdata["rating"], "comment": rdata["comment"]})

    print("🎉 SEEDING COMPLETE! 47+ Movies with UNIQUE Posters across Education, Horror, Crime, Patriotism, Mythology, Sports, Romance ready.")

if __name__ == "__main__":
    seed_data()
