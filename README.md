## 环境依赖：

1、python >=3.6
2、第三方库 gast >=0.3.3
3、第三方库 ast >=0.8.1
4、第三方库 eventlet >=0.25.2
5、第三方库 astor <= 0.7.0 (gast处理不了attribut storage)
6、shell 辅助工具 rsync 用于替换 cp

## 使用方法：
注意：input如果为模型目录，请保证模型目录下的运行脚本可以正常运行，所需要的依赖都正常安装；
```
cd paddle_api_upgrade
sh run.sh input output

#input: 输入为需要升级的python脚本文件名，或者需要升级的模块目录(工具会递归解析，并在output目录下生成新文件)
#output: 输出为升级后的文件，或者目录
```

script 说明：
1. convert_dict.py will use the original json file (../dict/data.json) directly converted from excel to generate the following two file by default

	../dict/modify.dict
	../dict/delete.dict

2. restore_comments_spaces.py could restore comments and space in source model file to transfered model file and save it to ./temp1 folder.

	python restore_comments_spaces.py [original model folder or file path] [transfered model file without comments]

3. check_api.py could automaticly check whether an api could import into target environment or not and if not it will generate a summary report to record which api could not be included.

	cd paddle_api_upgrade/paddle_api_src/script/
	python check_api


test 说明： cd test run

	python TestNewApi.py 
	
	# currently we have unitest for each key word in dict
	
	test_add_kwarg
	test_delete_kwarg
	test_rename_kwarg
	test_fusion_def

	# test for transformer
	test_replace_full_name
	test_import_visitor

	# test_project_folder:
	bash run_mac.sh api_upgrade_src/tests/dygraph_folder_test/transformer/ api_upgrade_src/tests/dygraph_folder_test/output_folder_transformer/
	
	todo:

	test_single_model_file
	
