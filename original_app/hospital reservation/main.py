import os

PATIENT = "patient.csv"


class Human:
    def __init__(self, name):
        self.name = name #人の名前


class Patient(Human):
    """ Humanクラスの子クラス
    """
    def __init__(self, name, patient_id, symptom):
        super().__init__(name)
        self.patient_id = patient_id #患者のID
        self.symptom = symptom #症状


        pass


class Clinic:
    def __init__(self):
        self.patient_list = []

    def _check_reserved(self, patient):
        """患者の診断予約がすでにされているか確認
        """
        if patient in self.patient_list:
            return True
        return False


    def show_waiting_count(self):
        """ 診察待ち人数を表示
        """
        print(f'現在{len(self.patient_list)}人待ちです')
        
        

    def reserve(self, patient):
        """患者の予約を処理する
        """
    
        if self._check_reserved(patient):
            print(f'{patient.name}さんはすでに予約完了済みです。')

        else:
            self.patient_list.append(patient)
            print(f'{patient.name}さん予約完了しました。')


    def diagnosis(self, patient_id=None):
    """患者の診断処理をする。
    　　引数で患者を指定した時は、その患者を優先。
       指定なしの場合は、予約の早い患者から診断する。
    """




        pass

    def read_file(self):
        """患者予約一覧ファイル読み込み
        """
        if not os.path.exists(PATIENT):
            raise FileNotFoundError(f"{PATIENT}が見つかりません。")

        read_list = []
        with open(PATIENT, encoding="UTF-8") as read_file:
            for row in read_file:
                name, age, symptom = row.split(',')
                patient = Patient(name.strip(), age.strip(), symptom.strip())
                read_list.append(patient)
        return read_list

    
    def write_file(self, patient):
        """予約が完了したら、その旨を患者予約一覧ファイルに書き込む。
        """
        with open(PATIENT, 'a', encoding="UTF-8") as f:
            for row in f:
                if row in f:
                    f.write(f'row, 予約済み')
                    break


def main():

    myclinic = Clinic()

    patients = myclinic.read_file()

    # 予約処理
    for patient in patients:
        myclinic.reserve(patient)
        myclinic.write_file(patient)

    pass

    # 診察処理
    myclinic.diagnosis()
    
    myclinic.show_waiting_count()



    pass





if __name__ == "__main__":

    main()
