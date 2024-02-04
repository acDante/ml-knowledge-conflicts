"""Remove metadata in the MRQA dataset and keep only the question, answer and context fields

"""
import jsonlines
import argparse


def read_data(data_path):
    examples = []
    with jsonlines.open(data_path) as reader:
        for obj in reader:
            if "uid" in obj.keys():
                examples.append(obj)
    return examples

def clean_data(org_examples):
    processed_examples = []
    for sample in org_examples:
        processed_sample = {"question": sample['query'],
                            "context": sample['context'],
                            "answer": []}
        gold_answers = []
        for ans in sample['gold_answers']:
            gold_answers.append(ans['text'])
        
        processed_sample['answer'] = gold_answers
        processed_examples.append(processed_sample)

    assert len(processed_examples) == len(org_examples)
    return processed_examples

def main(args):
    org_examples = read_data(args.input_path)
    processed_examples = clean_data(org_examples)
    with jsonlines.open(args.output_path, "w") as writer:
        writer.write_all(processed_examples)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="Path to the MRQA dataset"
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to save the processed MRQA dataset"
    )
    args = parser.parse_args()
    main(args)
