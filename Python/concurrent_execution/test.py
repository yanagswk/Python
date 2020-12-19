# pythonからコマンド(lsやmkdirなど)を実行するためのモジュール
import subprocess

cmd = "ls -l"
# コマンドは半角スペース毎に配列で与える。
subprocess.call(cmd.split())

# check_call
# 実行時の出力、エラーは実行されたタイミングで出力される。
# 正常に実行された場合は０を返す
runcmd = subprocess.check_call(cmd.split())
print(runcmd)

# check_output
# 正常にコマンドが実行された場合、バイト文字で出力を返す
runcmd2 = subprocess.check_output(cmd.split())
print(runcmd2)

# _＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿________________________＿


# stdout 標準出力。実行結果を取得する場合に指定。
# stderr 標準エラー。実行結果を取得する場合に指定。
proc = subprocess.run(["ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(proc.stdout.decode('utf8'))
