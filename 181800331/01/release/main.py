# -*- coding: utf-8 -*-
"""
Created on 2020/9/12

@author: Tomspiano

@email: wengenhui.gracie@foxmail.com

@description: plagiarism detection
"""
import os
import sys
from gensim import corpora
import numpy as np
from .dcheck import process as pc, compare as cmp

stoplist = {
    '何处', '加以', '除', '以至于', '即', '而后', '宁可', '还', '二来', '为此', '照', '截至', '譬如', '同时', '为止', '除开', '继而', '惟其', '地', '难道说',
    '为', '各', '可是', '依据', '岂但', '当', '从', '如下', '就', '是以', '另一方面', '不若', '比如', '假若', '况且', '的话', '只怕', '加之', '着', '那些',
    '你', '诸如', '”', '她', '然则', '哪', '别的', '才', '哈', '顺着', '之一', '若夫', '了', '他人', '庶几', '犹自', '即便', '要不是', '呗', '紧接着',
    '既是', '如其', '于', '_', '上下', '这儿', '光是', '己', '诸', '论', '还是', '或者', '连', '基于', '固然', '倘然', '果然', '起', '不特', '啷当',
    '先不先', '焉', '仍', '到', '呜呼', '有的', '哪边', '吓', '越是', '其', '因为', '咱们', '只是', '其他', '哪怕', '总的来说', '何时', '于是', '每',
    '那么样', '前者', '是', '不尽', '向使', '唉', '打从', '按照', '至今', '不是', '开外', '矣', '不尽然', '来', '在于', '呵', '因着', '则', '这么些', '呵呵',
    '：', '漫说', '乘', '俺', '当然', '那样', '那里', '或', '比', '致', '关于', '不单', '一转眼', '为什么', '但', '只有', '对待', '大', '由此', '望',
    '啦', '果真', '甚至', '别管', '吧哒', '嘿', '您', '别说', '此间', '那时', '一样', '凭', '们', '可见', '一旦', '乃', '某某', '“', '至于', '虽说',
    '本地', '要不', '而言', '用', '由是', '能', '与', '非但', '比及', '莫如', '那个', '总而言之', '以便', '只', '但凡', '贼死', '云云', '嗡', '归齐', '他们',
    '只当', '赶', '这些', '如何', '也好', '很', '所', '至', '非独', '以为', '另悉', '于是乎', '人', '不成', '其中', '针对', '像', '一', '它', '这就是说',
    '任凭', '那儿', '嘎登', '有些', '喏', '另', '乎', '再', '这一来', '再说', '8', '3', '巴巴', '故', '这里', '并非', '什么', '随后', '个', '本人',
    '进而', '相对而言', '不仅', '何况', '这么点儿', '作为', '第', '之', '还要', '距', '恰恰相反', '哪样', '毋宁', '不外乎', '内', '有时', '哪个', '咧', '所有',
    '按', '叮咚', '当着', '本身', '咋', '因', '呀', '而是', '及', '反过来', '正巧', '看', '也罢', '依照', '几时', '离', '尽管如此', '是的', '随', '要是',
    '如同', '哩', '甚么', '多么', '最', '这样', '等', '宁肯', '自', '人家', '这般', '兮', '不论', '那边', '其一', '若果', '自己', '再者', '除外', '嗳',
    '不独', '开始', '这', '一何', '结果', '过', '以期', '使得', '对比', '自身', '自各儿', '不过', '唯有', '而已', '以免', '起见', '借', '正是', '为何', '管',
    '一则', '8', '有及', '遵照', '不拘', '综上所述', '哎呀', '嗡嗡', '来着', '若', '什么样', '这会儿', '只限', '宁愿', '一切', '对', '以及', '较', '即如',
    '在下', '甚且', '即令', '别人', '随时', '尚且', '以上', '其次', '出来', '某', '反过来说', '虽则', '同', '除非', '之类', '许多', '再有', '她们', '得',
    '谁知', '；', '甚至于', '本', '纵然', '咦', '在', '其二', '冒', '何以', '谁', '具体说来', '个别', '哪年', '何', '宁', '省得', '由此可见', '与其说', '好',
    '已', '欤', '咱', '待', '纵', '。', '、', '被', '换言之', '没奈何', '然而', '趁', '故而', '有', '说来', '那么些', '因了', '倘使', '且说', '所以',
    '至若', '乃至', '分别', '所幸', '不至于', '么', '多少', '逐步', '另外', '与此同时', '并且', '有关', '然后', '俺们', '哼', '鉴于', '既然', '吗', '替',
    '也', '不问', '随着', '自家', '1', '9', '对方', '就是说', '除此之外', '从此', '喔唷', '般的', '其它', '乌乎', '总的来看', '尔尔', '曾', '犹且', '如上',
    '去', '怎样', '不怕', '来自', '自后', '那会儿', '哪天', '兼之', '设使', '啪达', '便于', '此地', '除了', '今', '及至', '仍旧', '以至', '以故', '为了',
    '自个儿', '使', '鄙人', '巴', '与否', '设或', '你们', '呃', '亦', '照着', '哪儿', '尽管', '哟', '既', '阿', '这边', '来说', '各自', '一般', '5',
    '则甚', '就是了', '不如', '不得', '呕', '却', '首先', '及其', '不比', '$', '假使', '全部', '我们', '某个', '用来', '为着', '一方面', '时候', '多',
    '这时', '哪些', '孰知', '旁人', '依', '咚', '直到', '靠', '小', '受到', '啊', '而外', '并', '竟而', '啐', '朝', '他', '如若', '不料', '例如', '等等',
    '谁料', '据此', '给', '比方', '继后', '但是', '较之', '云尔', '人们', '之所以', '下', '呜', '一来', '者', '只要', '以来', '打', '由于', '本着', '倘或',
    '各个', '似的', '不只', '如是', '该', '临', '等到', '叫', '设若', '纵令', '任何', '或曰', '几', '别处', '呸', '类如', '譬喻', '边', '6', '接着',
    '矣哉', '嗯', '吱', '总的说来', '庶乎', '凡是', '不然', '而', '如上所述', '才能', '又及', '后者', '据', '极了', '经过', '矣乎', '嗬', '跟', '赖以',
    '哈哈', '根据', '其余', '对于', '嘎', '纵使', '非徒', '后', '呢', '哦', '咳', '倘若', '向', '各种', '怎么', '哪里', '！', '每当', '具体地说', '我',
    '彼时', '就要', '2', '正值', '沿着', '倘', '此', '全体', '以', '怎么办', '怎', '大家', '把', '继之', '这么样', '简言之', '出于', '莫若', '哼唷', '诚然',
    '乃至于', '已矣', '如', '尔', '让', '抑或', '不妨', '吧', '连同', '反之', '将', '此处', '啥', '不光', '而且', '遵循', '不但', '冲', '别是', '这么',
    '即使', '那般', '故此', '要', '即若', '总之', '或则', '由', '嘛', '莫不然', '儿', '着呢', '所在', '眨眼', '任', '归', '如此', '彼', '趁着', '?',
    '既往', '反而', '替代', '》', '嘻', '甚而', '都', '和', '或是', '拿', '还有', '余外', '4', '万一', '两者', '非特', '沿', '虽', '虽然', '处在', '些',
    '前后', '某些', '即或', '哎', '且不说', '《', '顺', '诚如', '且', '再者说', '通过', '这次', '可', '慢说', '假如', '傥然', '的确', '嘘', '尽', '喽',
    '上', '若非', '别', '谁人', '呼哧', '各位', '它们', '始而', '罢了', '此时', '无宁', '不', '若是', '向着', '凭借', '，', '嘿嘿', '再则', '无', '因此',
    '就是', '喂', '那', '哉', '此外', '以致', '就算', '一些', '不管', '哇', '此次', '不惟', '0', '那么', '前此', '要么', '尔后', '可以', '自打', '要不然',
    '能否', '介于', '诸位', '如果', '与其', '朝着', '甚或', '只消', '经', '否则', '腾', '得了', '无论', '哎哟', '？', '孰料', '又', '往', '从而', '怎么样',
    '正如', '自从', '而况', '再其次', '换句话说', '哗', '怎奈', '凡', '的', '这个', '彼此', '当地', '因而',
}

if __name__ == '__main__':
    # read command
    assert len(
            sys.argv) == 4, 'Please use the format: python main.py [original document] [document need to be checked] ' \
                            '[evaluation result]'
    assert os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]), 'Please check the path of the documents'
    ori_path = sys.argv[1]
    smp_path = sys.argv[2]
    rst_path = sys.argv[3]

    # process the documents
    path = [ori_path, smp_path]
    texts = pc.segment(path, stoplist)

    ori_dic = corpora.Dictionary([texts[0]])
    smp_dic = corpora.Dictionary([texts[1]])

    # get Jaccard index
    ori_set = set(ori_dic.token2id.keys())
    smp_set = set(smp_dic.token2id.keys())

    inter = ori_set & smp_set
    union = ori_set | smp_set

    jc = len(inter) / len(union)

    # get cosine similarity of the identical words
    total = np.array([len(text) for text in texts])
    frequency = cmp.get_tf(texts)

    tf = np.zeros((len(frequency), len(inter)))
    for i, word in enumerate(inter):
        for j, fq in enumerate(frequency):
            tf[j][i] = fq[word]
    for i, cnt in enumerate(total):
        tf[i] /= cnt

    cs = np.dot(tf[0], tf[1]) / (np.linalg.norm(tf[0]) * np.linalg.norm(tf[1]))

    # save the result
    rst = jc * cs
    # print('{:.2f}'.format(rst))
    with open(rst_path, 'w', encoding='utf-8') as f:
        f.write('{:.2f}'.format(rst))
