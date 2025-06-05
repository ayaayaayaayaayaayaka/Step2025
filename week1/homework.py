# %%
from collections import Counter

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
def calculate_score(word):
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score

#辞書の読み込みと下処理
#original_dic:辞書そのものをlistとして保存
def make_dic():
    file_path = '/Users/tawaraayaka/stepJapan/words.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        original_dic = [word.strip() for word in f if word.strip()]  # 空行を除いて改行ごとに読み込み
        
    dic = []
    for word in original_dic:
        word_counts = Counter(word)
        score = calculate_score(word)
        dic.append((word_counts,word,score))
    return dic


def input_count(size): 
    #input読み込み、処理
    file_path = f'/Users/tawaraayaka/stepJapan/{size}.txt'  # 読み込みたい.txtファイルのパスを指定
    with open(file_path, 'r', encoding='utf-8') as f:
        words = [word.strip() for word in f if word.strip()]  # 空行を除いて改行ごとに読み込み
    counts = []
    for word in words:
        counter = Counter(word)
        counts.append(counter)
    return counts


def find_formable_anagram(size,dic,counts): 
    #本処理
    #print(counts)
    with open(f"{size}_answer.txt", "w", encoding="utf-8") as f:
        ans = []
        for counter in counts:
            index = -1
            candidate = 0
            for word_info in dic:
                index += 1
                inner = True
                for key in word_info[0].keys():
                    if key not in counter.keys():
                        inner = not inner
                        break
                    elif word_info[0][key] > counter[key]:
                        inner = not inner
                        break
                if inner == True:
                    candidate_word = word_info[1]
                    score = word_info[2]
                    if (candidate < score):
                        candidate = score
                        ans_word = candidate_word
            f.write(ans_word + "\n") 
            ans.append(ans_word)
        return ans

def main():
    original_dic = make_dic()
    for size in ["small","medium","large"]:
        print(size + ".text's anagram is as follow.\n")
        print(find_formable_anagram(size,original_dic,input_count(size)))


if __name__ == "__main__":
    main()
    
# %%

def testcase_prepare():
    input_words = ["silent", "SiLent\n", "  ", "\n", "1a0pPle"]
    #通常？、小文字大文字混ざっているとき、inputが空白の時、空白の時2、数字が混ざっている時
    input_cleaned_words = []
    for word in input_words:
        cleaned = word.strip()
        if cleaned:
            cleaned = cleaned.lower()
            cleaned = ''.join([char for char in cleaned if not char.isdigit()])
            input_cleaned_words.append(cleaned)
        else:
            input_cleaned_words.append('')

    sorted_inputs = []
    for input_word in input_cleaned_words:
        sorted_input = ''.join(sorted(list(input_word)))
        sorted_inputs.append(sorted_input)

    return input_words, sorted_inputs

def dic_prepare():
    #辞書の読み込みと下処理
    #words:辞書そのものをlistとして保存
    file_path = '/Users/tawaraayaka/stepJapan/words.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        original_dic = [word.strip() for word in f if word.strip()]  # 空行を除いて改行ごとに読み込み
        
    #ここから色々していく
    #DBの下準備
    dic = []
    for word in original_dic:
        dic.append((''.join(sorted(list(word))),word))
    dic.sort()
    return dic

def anagram_binary_search(dic,sorted_input):
    left = 0
    right = len(dic) - 1
    ans = []
        
    while(left <= right):
        mid = (left + right) // 2
        half_word = dic[mid][0]
        #sorted_inputをsorted_word(<-dicの一要素目)の中から探していく        
        if(half_word == sorted_input):
            ans.append(dic[mid][1])
            i = mid + 1
            j = mid - 1
            if(i < len(dic)):
                while(dic[i][0] == sorted_input):
                    ans.append(dic[i][1])
                    i += 1
            if(j >= 0):
                while(dic[j][0] == sorted_input):
                    ans.append(dic[j][1])
                    j -= 1
            break
                #二分探索して合致すればその周りも探し出した
        if(half_word > sorted_input):
            right = mid - 1
        else:
            left = mid + 1
    return ans
            
def main():
    dic = dic_prepare()
    input_words, sorted_inputs = testcase_prepare()
    for input_word, sorted_input in zip(input_words, sorted_inputs):
        ans_list = anagram_binary_search(dic, sorted_input)
        if ans_list == []:
            print(f"{input_word} has no anagram")
        else:
            print(f"{input_word} has {len(ans_list)} anagram(s)")
            print(ans_list)

if __name__ == "__main__":
    main()

# %%
input_words, sorted_inputs = testcase_prepare()
print(input_words)
print(sorted_inputs)

# %%
