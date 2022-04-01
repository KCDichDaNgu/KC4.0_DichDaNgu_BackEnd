import random
import string
import sys

letters = string.ascii_letters
digits = string.digits
punc = string.punctuation
glitch = 'à̷̹̲̼̖̉̐̈͂̔b̶̼͚̈͐͐̄̕c̷̡̛̙̗̦̗̬̥̮̹̖̘̪̈̈́̓̓̈̈͐̊͑̋͋̄̇͝d̸̠͖̲͚̱̠̯̻̆͋̋̀̂͆̓̚̚͝͝e̵̛͉̠͎̎̈́̏̌̽f̸̨̱͔̹̺͇̄̈́̏͐̆̈ģ̸̳̌̄̈̊̆͌̉͂̈́̽ȟ̶̡͖̰͐̐͒̾̑̑̅͋̋̕̕͜͝i̶͙͉̟̠̪͔̾͗̿̋̕j̸̻̞̗̯͙̰̥͚͔̤̙̫̹̠̾͂̉̒̀̕͘͘͜k̵̘̰̪̻̜͕͙̀̊̋̊̊͊̌̃̽͑l̷̝̫͊͋̍̀̏m̵̧͖̼̝̭̄͗̈͑̀͊̅̃̈ņ̷̡͓̗̳̜̞̌̊̆̔͋͘͜o̶͎̝͓̟͈̖̊́̽̀͘͜ͅṗ̷͚̯͓̖͇̅͑͒͐͜͠q̵̨̯͈̣̪͎͚͔̜͔͒r̸̡̖̮̘̋̽̐̅́͠ş̴̘̣̱̎͌͜ṫ̵̡̛̮̱̖̞̋̒̇̕͝ü̷̬̗̠̩̫͇͇͕͓̿͛͆̾͘v̵̡̘̳̖̹͎̆̉́́̀̊̀̓̓̌͠w̴̭̩͙̜̼̭̮̥̫̼̉͆͊͗͒x̴͓̻̭͔̗̻̻̰͐͌͛y̴̖̗̞̪͒̄̄̽ͅz̵͚͖̜̼̦̖̲̝̔͋̌̄̈̐̈́͘͜ͅĂ̵̛̛̙͙̩̆̓̀̈́̄̋͗̊̽̚͝B̷̭̓͗͐C̷̡̙̞̜̗̘̰̼̠̀̿̄̾̀̄̍̌̇̅̔͆́͐̌D̴̼͍̞̪̯̹͚͈̋̀͛̇̒̍̈́͜͜͠͠E̷̼͐̑͗̈́͗̓́̽̚͝F̵̗̬̘̹̻̰̣̻͙͂̾̋̄̓̇̈́͊͐̀͑̋̄̀͜Ģ̶̧̨̧̩̼͍̻̠̥̦̲̜͛̏̈́͑̚͜͠ͅH̴͍̗̣͔̻̜̽̈́̂͋͑̾̽̀̿͆̉͘̕͝ͅI̸̢̦͇̦͙̣̪͍̪̺̒͑̈́̀͒͗̀̉̈́̽͝ͅJ̴̰̦͙͎̋̌̊͐͊̓̂́K̴̡̬̗̙̞̝͕͕̯̪̯̣͚̟̓͋͑̏̽̆̽͆̾L̶̢̯̺̳̮̮̮̯̲͔̺͔͂͋̇̐̏́̋̏̌̏̀M̷̢̻͚̙̬͎͕͓̫̜̣̳̙͐̀̅͐̃̂͋́̚͠Ṇ̷̰̬̰͍͍͕̱͍̬̓́̕̕͠Ǫ̷͍̬̖̮͓͙̰͇̊̆̅̽̑́͌̆̑͗̚Ṗ̷̛̝͙̲̼̼̀͗́͛̂̈́̿̈́͌͒͘͝Q̶̡̙̦͖̬̪̯̖͈̂̀̅͘̚͝Ŗ̵̩͒̉͐́͊̿̀̈́͗̒͑̉͝͝Ş̷̡͎̩̯͕̭͇͕͐̀̊̏̀̈́̅̿͜͝͝T̶̡͔͙͎̙͖̥̜͇͍̪̳̰̻̒̔͊̂̅́̽̅̚̚̚͘͜U̴̺̝͐́̚V̴̢̛̲͔͈̦͖̳̯͚̗̼̬͖̹̦̾͌̊̈́͐̄̉̔͐̓̂͌̈́͘W̴͔̬̖͚̪̠͈̫̊̍̃̅̊̀̌̑͂̍̈́̓̉͂X̶̛̱̗̖̖̯̜̰͔̦̳̋̾͑̈́͋̋̔͝Y̷̛̺̦͉̦͔̲̟̩̗̰̼͍̩̍̐͜ͅZ̵̦̖̹̭̹͍̗̻̺̻̏̅̄̕͝'
emote = '😀😃😄😁😆😅😂🤣🥲☺️😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🥸🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽🙀😿😾'

random_seed = 271828
random.seed(random_seed)


# Create tests contains only letters
def create_letters_tests(count: int, max_length: int):
    # Create random strings as tests
    tests = []
    for _ in range(count):
        tests.append(''.join(random.choices(
            letters + ' \n', k=random.randint(1, max_length)
        )))

    # Write test to file
    for i in range(count):
        with open(f'./testcases/lettertest_{i}.txt', 'w+') as f:
            f.write(tests[i])
            print(f'Created test file lettertest_{i}.txt in ./testcases/')

    return tests


# Create tests contains only digits
def create_digit_tests(count: int, max_length: int):
    # Create random strings as tests
    tests = []
    for _ in range(count):
        tests.append(''.join(random.choices(
            digits + ' \n', k=random.randint(1, max_length)
        )))

    # Write test to file
    for i in range(count):
        with open(f'./testcases/digitest_{i}.txt', 'w+') as f:
            f.write(tests[i])
            print(f'Created test file digitest_{i}.txt in ./testcases/')

    return tests


# Create tests contains only punctuations
def create_punc_tests(count: int, max_length: int):
    # Create random strings as tests
    tests = []
    for _ in range(count):
        tests.append(''.join(random.choices(
            punc + ' \n', k=random.randint(1, max_length)
        )))

    # Write test to file
    for i in range(count):
        with open(f'./testcases/punctest_{i}.txt', 'w+') as f:
            f.write(tests[i])
            print(f'Created test file punctest_{i}.txt in ./testcases/')

    return tests


# Create tests contains only glitch letters
def create_glitch_tests(count: int, max_length: int):
    # Create random strings as tests
    tests = []
    for _ in range(count):
        tests.append(''.join(random.choices(
            glitch + ' \n', k=random.randint(1, max_length)
        )))

    # Write test to file
    for i in range(count):
        with open(f'./testcases/glitchtest_{i}.txt', 'w+') as f:
            f.write(tests[i])
            print(f'Created test file glitchtest_{i}.txt in ./testcases/')

    return tests


# Create tests contains only emotes
def create_emote_tests(count: int, max_length: int):
    # Create random strings as tests
    tests = []
    for _ in range(count):
        tests.append(''.join(random.choices(
            emote + ' \n', k=random.randint(1, max_length)
        )))

    # Write test to file
    for i in range(count):
        with open(f'./testcases/emotestest_{i}.txt', 'w+') as f:
            f.write(tests[i])
            print(f'Created test file emotestest_{i}.txt in ./testcases/')

    return tests


# Create tests contains all above cases
def create_full_tests(count: int, max_length: int):
    # Create random strings as tests
    tests = []
    for _ in range(count):
        tests.append(''.join(random.choices(
            letters + digits + punc + glitch + emote + ' \n', k=random.randint(1, max_length)
        )))

    # Write test to file
    for i in range(count):
        with open(f'./testcases/fulltest_{i}.txt', 'w+') as f:
            f.write(tests[i])
            print(f'Created test file fulltest_{i}.txt in ./testcases/')

    return tests


# Create normal test cases
def create_normal_tests():
    # Create random strings as tests
    tests = []
    tests.append("The bully at school was mean to everyone except me.\nWe're leaving in ten minutes, whether you're dressed or not.\nThe girl wore her hair in two braids, tied with two blue bows.")
    tests.append("ການຂົ່ມເຫັງຢູ່ໃນໂຮງຮຽນແມ່ນມີຄວາມຫມາຍສໍາລັບທຸກຄົນຍົກເວັ້ນຂ້ອຍ.\nພວກເຮົາອອກໄປໃນສິບນາທີ, ບໍ່ວ່າເຈົ້າຈະນຸ່ງຫລືບໍ່.\nເດັກຍິງໃສ່ຜົມຂອງນາງໃນສອງ braids, ມັດດ້ວຍ bows ສີຟ້າສອງ.")
    tests.append("學校裡的惡霸對除了我以外的所有人都很刻薄。 不管你穿好不穿，我們十分鐘後離開。 這個女孩把頭髮編成兩條辮子，用兩個藍色蝴蝶結繫著。")
    tests.append("ការបៀតបៀននៅសាលាគឺអាក្រក់សម្រាប់មនុស្សគ្រប់គ្នា លើកលែងតែខ្ញុំ។ យើង​នឹង​ចេញ​ក្នុង​រយៈ​ពេល​ដប់​នាទី មិន​ថា​អ្នក​ស្លៀកពាក់​ឬ​អត់។ ក្មេងស្រីពាក់សក់របស់នាងជាខ្ចោពីរ ចងដោយធ្នូពណ៌ខៀវពីរ។")
    tests.append(
        "学校里的恶霸对除了我以外的所有人都很刻薄。 不管你穿好不穿，我们十分钟后离开。 这个女孩把头发编成两条辫子，用两个蓝色蝴蝶结系着。")
    tests.append("Today I dressed my unicorn in preparation for the race. For some unfathomable reason, the response team didn't consider a lack of milk for my cereal as a proper emergency. The changing of down comforters to cotton bedspreads always meant the squirrels had returned.")
    tests.append("Hoy vestí a mi unicornio en preparación para la carrera.\n\tPor alguna razón insondable, el equipo de respuesta no consideró la falta de leche para mi cereal como una emergencia adecuada.\n\tEl cambio de edredones de plumas por cubrecamas de algodón siempre significaba que las ardillas habían regresado.")
    tests.append("Өнөөдөр би уралдааны бэлтгэлд зориулж ганц эвэртээ өмсөв.\n\tЯмар нэг ойлгомжгүй шалтгааны улмаас хариу арга хэмжээ авах баг миний үр тарианы сүү дутагдаж байгааг яаралтай тусламж гэж үзээгүй.\n\tХөвөн даавуун орны даавуугаар хөнжил сольсон нь хэрэм буцаж ирсэн гэсэн үг.")
    tests.append("Aujourd'hui j'ai habillé ma licorne en préparation de la course. Pour une raison insondable, l'équipe d'intervention n'a pas considéré le manque de lait pour mes céréales comme une véritable urgence.\n\tLe remplacement des couettes en duvet par des couvre-lits en coton signifiait toujours le retour des écureuils.")
    tests.append("ថ្ងៃនេះ ខ្ញុំបានស្លៀកពាក់ unicorn របស់ខ្ញុំ ដើម្បីត្រៀមខ្លួនសម្រាប់ការប្រណាំង។ សម្រាប់ហេតុផលដែលមិនអាចយល់បាន ក្រុមការងារឆ្លើយតបមិនបានចាត់ទុកការខ្វះទឹកដោះគោសម្រាប់ធញ្ញជាតិរបស់ខ្ញុំថាជាគ្រាអាសន្នត្រឹមត្រូវ។ ការ​ផ្លាស់​ប្តូរ​ភួយ​មក​ជា​ក្រណាត់​កប្បាស​តែងតែ​មាន​ន័យ​ថា​សត្វ​កំប្រុក​បាន​វិល​មក​វិញ។")
    tests.append("ມື້​ນີ້​ຂ້າ​ພະ​ເຈົ້າ​ນຸ່ງ unicorn ຂອງ​ຂ້າ​ພະ​ເຈົ້າ​ໃນ​ການ​ກະ​ກຽມ​ສໍາ​ລັບ​ການ​ແຂ່ງ​ຂັນ​. ສໍາລັບເຫດຜົນທີ່ບໍ່ເຂົ້າໃຈໄດ້ບາງອັນ, ທີມງານຕອບສະຫນອງບໍ່ໄດ້ພິຈາລະນາການຂາດນ້ໍານົມສໍາລັບຫານປະເພດເມັດຂອງຂ້ອຍເປັນເຫດສຸກເສີນທີ່ເຫມາະສົມ. ການປ່ຽນຜ້າປູບ່ອນນອນເປັນຜ້າປູທີ່ນອນສະເໝີໝາຍຄວາມວ່າກະຮອກໄດ້ກັບຄືນມາ.")

    # Write test to file
    for i in range(len(tests)):
        with open(f'./testcases/normaltest_{i}.txt', 'w+') as f:
            f.write(tests[i])
            print(f'Created test file normaltest_{i}.txt in ./testcases/')

    return tests


# Driver function
def run():
    print(f'Generating test cases with seed {random_seed} ...')
    create_letters_tests(count=5, max_length=100)
    create_digit_tests(count=5, max_length=100)
    create_punc_tests(count=5, max_length=100)
    create_glitch_tests(count=5, max_length=100)
    create_emote_tests(count=5, max_length=100)
    create_full_tests(count=5, max_length=100)
    create_normal_tests()


if __name__ == "__main__":
    # Read seed argument
    if len(sys.argv) >= 2:
        if sys.argv[1].isdigit():
            random_seed = int(sys.argv[1])
    run()
