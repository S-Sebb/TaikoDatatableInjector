# -*- coding: utf-8 -*-
from utils import *

init()

inject_data_list, extract_data_list = get_datatable_files()

modified_data_list = []

# write the injection logic here

write_datatable_files(tuple(modified_data_list))
