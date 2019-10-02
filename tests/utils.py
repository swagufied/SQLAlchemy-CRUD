def block_msg(msg, *args):
	msg = msg % args
	print("\n\n\n" + "-" * len(msg.split("\n")[0]))
	print(msg)
	print("-" * len(msg.split("\n")[0]))