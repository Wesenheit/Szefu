import os
import discord 

def list():
    forbiden=['.d',".py",".git"]
    files=os.listdir()
    for file in files:
        temp=True
        for end in forbiden:
            if end in file:
                temp=False
            if "." not in file:
                temp=False
        if temp:
            yield file


def cleanup():
    for file in list():
        os.remove(file)

def size():
    return sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))


async def autocleanup(ctx,n):
    if size()>n:
        cleanup()
    await ctx.send("Przekroczono maksymalny rozmiar piosenek, trwa ich usuwanie")
    