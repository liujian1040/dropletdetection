# -*- coding: utf-8 -*-
import json
import os
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default="./val", help="Path to Image Directory")
    parser.add_argument("--output_path", type=str, default="./val", help="Path to Image Directory")

    opt = parser.parse_args()
    print(opt)

    input_path = opt.input_path
    output_path = opt.output_path

    l = os.listdir(input_path)
    l = [i for i in l if i.endswith('.json')]

    for i in l:
        with open(input_path + "\\" + i, 'r', encoding='utf-8') as f:
            temp = json.loads(f.read())
            anno = temp['shapes']
            new_anno = []
            for instance in anno:
                if instance['label'] == 'B':
                    instance['label'] = 'D'
                new_anno.append(instance)
            temp['shapes'] = new_anno
        with open(output_path + "\\" + i, 'w+', encoding='utf-8') as f:
            json.dump(temp, f)


