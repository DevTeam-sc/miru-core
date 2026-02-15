import miru

system_session = miru.attach(0)
bytecode = system_session.compile_script(
    name="bytecode-example",
    source="""\
rpc.exports = {
  listThreads: function () {
    return Process.enumerateThreadsSync();
  }
};
""",
)

session = miru.attach("Twitter")
script = session.create_script_from_bytes(bytecode)
script.load()
api = script.exports_sync
print("api.list_threads() =>", api.list_threads())
