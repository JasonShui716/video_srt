import srt
import sys
import deepl
import os

auth_key = os.environ["DEEPL_KEY"]
translator = deepl.Translator(auth_key)

END_PUNC_LIST=".;!?"

def handle_srt(data):
    tmp_srt_list = list()
    srt_list = list()
    for sub in srt.parse(data):
        if sub.content[-1] not in END_PUNC_LIST:
            tmp_srt_list.append(sub)
        else:
            if tmp_srt_list:
                tmp_str = ""
                tmp_srt_list.append(sub)
                for tmp_sub in tmp_srt_list:
                    tmp_str += tmp_sub.content.replace("\n", " ") + " "
                srt_list.append(srt.Subtitle(tmp_srt_list[0].index, tmp_srt_list[0].start, tmp_srt_list[-1].end, tmp_str))
                tmp_srt_list = []
            else:
                srt_list.append(sub)
    srt.sort_and_reindex(srt_list)
    for sub in srt_list:
        translation = translator.translate_text(sub.content, target_lang="ZH")
        sub.content += "\n" + translation.text
        print(sub.content)

    return srt.compose(srt_list) 

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        res = handle_srt(f.read())
        with open(sys.argv[1] + '.new', "w") as wf:
            wf.write(res)
