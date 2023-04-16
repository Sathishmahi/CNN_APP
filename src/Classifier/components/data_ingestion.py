import os
from urllib import request as req
from zipfile import ZipFile as zip
from Classifier.config import Configuration
from Classifier.utils import create_directories
from Classifier import logger
from Classifier.utils import get_size
from tqdm import tqdm
from pathlib import Path
import shutil

class DataIngestion:
    def __init__(self, Config: Configuration = Configuration()):
        self.data_injectioin_config = Config.data_ingestion_config

    def download_data(self):
        logger.info(f"try to download file ...")
        download_url = self.data_injectioin_config.source_URL
        local_data_file = self.data_injectioin_config.local_data_file
        folder, _ = local_data_dir = os.path.split(local_data_file)
        create_directories([folder], True)
        if not os.path.exists(path=local_data_file):
            logger.info(f"start download file ")
            req.urlretrieve(url=download_url, filename=local_data_file)
            logger.info(f"finish download file path is {local_data_file}")
        else:
            logger.info(f" file already exist - existing file path {local_data_file}")
            logger.info(
                f" file already exist - file size is  {get_size(Path(local_data_file))}"
            )

    def _extract_helper(self, path: str, zip_file_names: list, zf,seperate_valid_imgs=True):
        
        for file_name in tqdm(zip_file_names):
            base_name=os.path.basename(os.path.dirname(file_name))
            dir_name=os.path.join(path,'PetImages',base_name)
            create_directories([dir_name])            
            zf.extract(file_name, path=path)
            over_all_path = Path(os.path.join(path, file_name))
            if os.path.getsize(over_all_path)== 0:
                logger.info(f"remove file  file path is {over_all_path} ")
                os.remove(over_all_path)

    def _to_reduce_images(self,no_of_images_wants=100,delete_or_not=False,des_path=None):

        root_path='artifacts/data_ingestion/un_zip_dir/PetImages'

        [os.makedirs(os.path.join(root_path,i),exist_ok=True) for i in ['dog','cat']]

        for dir in [os.path.join(root_path,'Dog'),os.path.join(root_path,'Cat')]:
            if 'Cat' in dir:
                [shutil.move(os.path.join(dir,img_path),os.path.join(root_path,"cat")) for img_path in os.listdir(dir)[:no_of_images_wants] ]
            else:
                [shutil.move(os.path.join(dir,img_path),os.path.join(root_path,"dog")) for img_path in os.listdir(dir)[:no_of_images_wants] ]
            if not delete_or_not and des_path:

                shutil.move(dir,des_path)
            else:
                shutil.rmtree(dir)
    def _to_seperate_valid_images(self,artifacts_root_dir_name="artifacts",dir_name="valid_data",
                                unzip_dir_path=None,n_of_imgs=50):

        valid_root_path=os.path.join(artifacts_root_dir_name,dir_name)
        create_directories([valid_root_path])
        main_path=os.path.join(unzip_dir_path,os.listdir(unzip_dir_path)[0])
        for sub_dir in os.listdir(main_path):
            
            for img in os.listdir(os.path.join(main_path,sub_dir))[:n_of_imgs]:
                des_path=os.path.join(valid_root_path,sub_dir)
                create_directories([des_path])
                if not os.path.exists(os.path.join(des_path,img)):
                    shutil.move(os.path.join(main_path,sub_dir,img),des_path)
        


    def extract_data(self):
        logger.info(f"unzip started...")
        unzip_dir = self.data_injectioin_config.unzip_dir
        create_directories(path_to_directories=[unzip_dir])
        local_data_file = self.data_injectioin_config.local_data_file
        eval_dir_name=self.data_injectioin_config.eval_dir
        with zip(local_data_file) as zf:
            all_content_name_list = zf.namelist()
            all_filters_name = [
                name
                for name in all_content_name_list
                if name.endswith(".jpg") and ("Dog" in name or "Cat" in name)
            ]
            self._extract_helper(path=unzip_dir, zip_file_names=all_filters_name, zf=zf)
        root_dir=self.data_injectioin_config.root_dir
        des_path=os.path.join(root_dir,"all_images")
        self._to_reduce_images(des_path=des_path,no_of_images_wants=100)
        self._to_seperate_valid_images(unzip_dir_path=unzip_dir,dir_name=os.path.basename(eval_dir_name))
        logger.info(f"finish unzip")
