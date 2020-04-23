from django.db import models

# Create your models here.
class waste_div(models.Model):
    waste_div_no = models.IntegerField(primary_key=True)
    waste_div_name = models.CharField(max_length=30)
    
    def __str__(self):
        return [self.waste_div_no, self.waste_div_name]

class waste_type(models.Model):
    waste_type_no = models.IntegerField(primary_key=True)
    waste_type_waste_div_no = models.IntegerField()
    waste_type_name = models.CharField(max_length=30)
    waste_type_kor_name = models.CharField(max_length=30)
    waste_type_size = models.CharField(max_length=30)
    waste_type_fee = models.CharField(max_length=30)
    waste_type_area_no = models.IntegerField()
    
    #def __str__(self):
     #   return [self.waste_type_no, self.waste_type_waste_div_no, self.waste_type_name, self.waste_type_kor_name, self.waste_type_size, self.waste_type_fee, self.waste_type_area_no]
        #return self
    
class user_info(models.Model):
    user_info_no = models.IntegerField(primary_key=True)
    user_info_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self
class board_review(models.Model):
    board_review_no = models.IntegerField(primary_key=True)
    board_revie_board_no = models.IntegerField()
    board_review_ctnt = models.CharField(max_length=30)
    board_review_reg_user_no = models.IntegerField()
    board_review_reg_date = models.CharField(max_length=30) 

    def __str__(self):
        return self
class board(models.Model):
    board_no = models.IntegerField(primary_key=True)
    board_title = models.CharField(max_length=30)
    board_ctnt = models.CharField(max_length=30)
    board_reg_user_no = models.IntegerField()
    board_reg_date = models.CharField(max_length=30) 
    board_waste_area_no = models.IntegerField()

    def __str__(self):
        return self
class area(models.Model):
    area_no = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=30)
    area_name2 = models.CharField(max_length=30)
    area_address = models.CharField(max_length=30) 
    
    def __str__(self):
        return self
class apply_info(models.Model):
    apply_info_no = models.IntegerField(primary_key=True)
    apply_info_name = models.CharField(max_length=30)
    apply_info_address = models.CharField(max_length=30)
    apply_info_phone = models.CharField(max_length=30) 
    apply_info_waste_type_no = models.IntegerField()
    apply_info_fee = models.CharField(max_length=30) 
    apply_info_code = models.CharField(max_length=30) 
    apply_info_user_no = models.IntegerField()
    
    def __str__(self):
        return self
    

    