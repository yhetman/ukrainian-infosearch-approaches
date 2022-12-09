import os
import string
import sys
import time


class SPIMI(object):
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.overhead_parameter = 10000 * 512
        self.block_files = []
        self.docs = dict()
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)


    def list_directory(self, root):
        files_in_dir = [os.path.abspath(os.path.join(root, file)) for file in os.listdir(root)]
        self.docs = dict(zip(files_in_dir, list(range(len(files_in_dir)))))
        return files_in_dir


    def file_reading(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        return file_content


    def is_ukrainian(self, token):
        ukrainian = [96, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1100, 1102, 1103, 1108, 1110, 1111, 1169, 8217]
        for char in token:
            if ord(char) not in ukrainian:
                return False
        return True

    
    def tokenizer(self, file_content):
        return list(set([token for token in file_content.split() if token != '' and self.is_ukrainian(token) == True]))

    
    def linguistic_transform(self, file_content):
        punc = '''!()-'”№[]{};:"\\,“«»<>./?@#$%—…^&*_~|–abcdefghijklmnoqprstuvwxyz'''
        content = "".join([c for c in file_content.lower() if c not in punc])
        return content.translate(str.maketrans('', '', string.digits))
 
    def add_to_dictionary(self, dictionary, term):
        dictionary[term] = []
        return dictionary[term]

    def get_postings_list(self, dictionary, term):
        return dictionary[term]

    def add_to_postings_list(self, postings_list, doc_id):
        postings_list.append(doc_id)

    def spimi_invert(self, root, block_size=1000000):
        files_in_dir = self.list_directory(root)
        block_num = 0
        max_byte = block_size * 512
        current_size = 0
        self.previous_dictionary = {}
        self.dictionary = {}
        self.start_time = time.time()
        for doc_id in (files_in_dir):
            file_content = self.file_reading(doc_id)
            tokens = self.tokenizer(self.linguistic_transform(file_content))
            for token in tokens:
                if token not in self.dictionary:
                    current_size += sys.getsizeof(token)
                    postings_list = self.add_to_dictionary(self.dictionary, token)
                else:
                    postings_list = self.get_postings_list(self.dictionary, token)
                if current_size + sys.getsizeof(doc_id) > max_byte:
                    self.write_block(self.dictionary, block_num)
                    self.block_time(block_num, current_size / 512)
                    block_num += 1
                    self.dictionary = {}
                    current_size = 0
                    current_size += sys.getsizeof(token)
                    postings_list = self.add_to_dictionary(self.dictionary, token)
                    current_size += sys.getsizeof(doc_id)
                    self.add_to_postings_list(postings_list, self.docs[doc_id])
                else:
                    current_size += sys.getsizeof(doc_id)
                    self.add_to_postings_list(postings_list, self.docs[doc_id])
        if bool(self.dictionary):
            self.write_block(self.dictionary, block_num)
            self.block_time(block_num, current_size / 512)


    def block_time(self, block_num, block_size):
        end_time = time.time()
        print(f'BLOCK{block_num} with size: {round((block_size/ (1024 * 1024)), 1):.2f} MB =>  Time Taken for BLOCK {block_num}: {(end_time - self.start_time):.3f} sec')
        self.start_time = time.time()


    def write_block(self, dictionary, block_num):
        sorted_terms = [term for term in sorted(dictionary)]
        output_block_file = os.path.join(self.output_dir, f'BLOCK{block_num}.txt')
        with open(output_block_file, 'w', encoding='utf-8') as f:
            for term in sorted_terms:
                f.write(f'{term} {" ".join([str(doc_id) for doc_id in dictionary[term]])}\n')
        self.block_files.append(output_block_file)
        return output_block_file


    def write_compressed_block(self, dictionary, pointers, posting_list, block_num):
        terms = [dictionary[pointers[i]:pointers[i+1]-1] for i in range(len(pointers)-1)]
        sorted_terms = sorted(terms)
        output_block_file = os.path.join(self.output_dir, f'BLOCK{block_num}.txt')
        with open(output_block_file, 'w', encoding='utf8') as f:
            for i in range(len(sorted_terms)):
                term_index = terms.index(sorted_terms[i])
                line = f'{sorted_terms[i]} {" ".join([str(doc_id) for doc_id in posting_list[term_index]])}\n'
                f.write(line)
        self.block_files.append(output_block_file)
        return output_block_file


    def spimi_merge(self, output_file):
        opened_block_files = [open(block_file, encoding='utf-8') for block_file in self.block_files]
        file_lines = [block_file.readline()[:-1] for block_file in opened_block_files]
        prev_term = ''
        first_line = True
        with open(output_file, 'w', encoding='utf-8') as f:
            while (len(opened_block_files)) > 0:
                first_index = file_lines.index(min(file_lines))
                line = file_lines[first_index]
                curr_term = line.split()[0]
                curr_postings = ' '.join(line.split()[1:])
                if curr_term != prev_term:
                    if first_line:
                        f.write(f'{curr_term} {curr_postings}')
                        first_line = False
                    else:
                        f.write(f'\n{curr_term} {curr_postings}')
                    prev_term = curr_term
                else:
                    f.write(f' {curr_postings}')
                file_lines[first_index] = opened_block_files[first_index].readline()[:-1]
                if file_lines[first_index] == '':
                    opened_block_files[first_index].close()
                    opened_block_files.pop(first_index)
                    file_lines.pop(first_index)
        return True



    def spimi_compress_dictionary(self, root, block_size=100000):
        files_in_dir = self.list_directory(root)
        block_num = 0
        max_byte = block_size * 512
        current_size = 0
        self.start_time = time.time()
        self.dictionary = '|'
        self.pointers = []
        self.posting_lists = []
        for doc_id in (files_in_dir):
            file_content = self.file_reading(doc_id)
            tokens = self.tokenizer(self.linguistic_transform(file_content))
            for token in tokens:
                if f'|{token}|' not in self.dictionary:
                    current_size += sys.getsizeof(token)
                    self.pointers.append(len(self.dictionary))
                    self.dictionary += f'{token}|'
                    self.posting_lists.append([])
                    postings_list = self.posting_lists[-1]
                else:
                    pos_in_dict = self.pointers.index(self.dictionary.index(f'|{token}|')+1)
                    postings_list = self.posting_lists[pos_in_dict-1]
                if current_size + sys.getsizeof(doc_id) > max_byte:
                    self.write_compressed_block(self.dictionary, self.pointers, self.posting_lists, block_num)
                    self.block_time(block_num, current_size/512)
                    block_num += 1
                    self.dictionary = '|'
                    self.pointers = []
                    self.posting_lists = []
                    current_size = 0
                    current_size += sys.getsizeof(token)
                    self.pointers.append(len(self.dictionary))
                    self.dictionary += token
                    self.posting_lists.append([])
                    postings_list = self.posting_lists[-1]
                    current_size += sys.getsizeof(doc_id)
                    postings_list.append(doc_id)
                else:
                    current_size += sys.getsizeof(doc_id)
                    postings_list.append(doc_id)
        if bool(self.dictionary):
            self.write_compressed_block(self.dictionary, self.pointers, self.posting_lists, block_num)
            self.block_time(block_num, current_size / 512)


    def spimi_index(self, root, output_file, block_size=1000000):
        index_start_time = time.time()
        print('Starting Single-Pass In-Memory Indexing')
        self.spimi_invert(root, block_size)
        merge_start_invert_end_time = time.time()
        print(f'Invert Completed => Time Taken: {merge_start_invert_end_time - index_start_time:.3f} sec')
        print(f'Starting Merge of {len(self.block_files)} BLOCK files')
        self.spimi_merge(output_file)
        index_end_time = time.time()
        print(f'Merge Completed => Time Taken: {index_end_time - merge_start_invert_end_time:.3f} sec')
        print(f'Indexing Completed! Find index file at {output_file} => Time Taken: {index_end_time - index_start_time:.3f} sec')
        

    def spimi_compression_index(self, root, output_file, block_size=1000000):
        index_start_time = time.time()
        print('Starting Single-Pass In-Memory Indexing with Compression')
        self.spimi_compress_dictionary(root, block_size)
        merge_start_invert_end_time = time.time()
        print(f'Invert Completed => Time Taken: {merge_start_invert_end_time - index_start_time:.3f} sec')
        print(f'Starting Merge of {len(self.block_files)} BLOCK files')
        self.spimi_merge(output_file)
        index_end_time = time.time()
        print(f'Merge Completed => Time Taken: {index_end_time - merge_start_invert_end_time:.3f} sec')
        print(f'Indexing Completed! Find index file at {output_file} => Time Taken: {index_end_time - index_start_time:.3f} sec')
        


if __name__ == '__main__':
    spimi = SPIMI('./BLOCKS_NOCOMP')
    spimi.spimi_index('../books/','./INDEX/index_without_compression.txt', block_size=10000000)
    spimi = SPIMI('./BLOCKS')
    spimi.spimi_compression_index('../books/','./INDEX/index_with_compression.txt', block_size=100000)
