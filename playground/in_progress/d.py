import beaker as bk
import pyteal as pt
import typing
from beaker.lib.storage import BoxMapping,BoxList
# from beaker.lib.storage import BoxList



class Mystate:
    result = bk.GlobalStateValue(pt.TealType.uint64)

class Proposal_Record(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    proposal_name:pt.abi.Field[pt.abi.String]=[]
    asset_count:pt.abi.Field[pt.abi.Uint64]=[]
    asset_id:pt.abi.Field[pt.abi.String]=[]
    # asset_list = BoxList(asset_id,200)
    Amount:pt.abi.Field[pt.abi.Uint64]=[]
    descr = "record stored"

class asset_store(pt.abi.NamedTuple):
    #  proposal_id:pt.abi.Field[pt.abi.String]
     asset_id:pt.abi.Field[pt.abi.String]=[]
    
class User_per_proposal_record(pt.abi.NamedTuple):
    proposal_id:pt.abi.Field[pt.abi.String]
    user_id:pt.abi.Field[pt.abi.String]
    

class User_asset_store(pt.abi.NamedTuple):
    user_id:pt.abi.Field[pt.abi.String]
    asset_id:pt.abi.Field[pt.abi.String]
    User_Token:pt.abi.Field[pt.abi.Uint64]


class Response_store(pt.abi.NamedTuple):
    user_id:pt.abi.Field[pt.abi.String]
    asset_id:pt.abi.Field[pt.abi.String]
    User_Token:pt.abi.Field[pt.abi.Uint64]
    user_response:pt.abi.Field[pt.abi.Bool]



class Proposal_Record_State:
    proposal_rec = BoxMapping(pt.abi.String,Proposal_Record)
    user_rec = BoxMapping(pt.abi.String,User_per_proposal_record,prefix=pt.Bytes("_"))
    asset_rec = BoxMapping(pt.abi.String,User_asset_store,prefix=pt.Bytes("#"))
    response_rec = BoxMapping(pt.abi.String,Response_store,prefix=pt.Bytes("@"))
    asset_str = BoxMapping(pt.abi.String,asset_store,prefix=pt.Bytes("$"))
    # asset_list = BoxList(asset_id)
    yes_count = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
        descr="variable to store user response"
    )
    No_count = bk.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
        descr="variable to store user response"
    )
   


app =(
     bk.Application("Voting_Contract_fn_test",state = Proposal_Record_State())
     .apply(bk.unconditional_create_approval,initialize_global_state=True)
)



@app.external
def Register_proposal(proposal_id:pt.abi.String,proposal_name:pt.abi.String,asset_count:pt.abi.Uint64,asset_id:pt.abi.String,Amount:pt.abi.Uint64,* ,output:Proposal_Record) -> pt.Expr:
    
    proposal_store = Proposal_Record()

  
    return pt.Seq(

        proposal_store.set(proposal_id,proposal_name,asset_count,asset_id,Amount),
        pt.Assert(app.state.proposal_rec[proposal_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"),
        app.state.proposal_rec[proposal_id.get()].set(proposal_store),
        app.state.proposal_rec[proposal_id.get()].store_into(output),


    )


@app.external

def asset_register(proposal_id:pt.abi.String,asset_id:pt.abi.String,*,output:asset_store)->pt.Expr:
    proposal_get = Proposal_Record()
    asset_get = asset_store()

    return pt.Seq(
        proposal_get.decode(app.state.proposal_rec[proposal_id.get()].get()),
        asset_get.set(asset_id),
        pt.Assert(app.state.proposal_rec[asset_id.get()].exists()== pt.Int(0),comment="Proposal_ID already exists"),
        app.state.asset_str[(asset_id).get()].set(asset_get),
        app.state.asset_str[asset_id.get()].store_into(output),


        

    )
if __name__=="__main__":
    
    spec=app.build()
    
    spec.export("artifacts_test_2")
