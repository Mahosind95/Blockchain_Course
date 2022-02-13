# Blockchain_Course
This is my first attempt to learn blockchain

**Blockchain.py** contains all the basic building blocks for any blockchain
  - __init__ : This method creates the genesis block of the blockchain
  - create_block() : adds a new block to block chain
  - get_previous_block() : gets the previous block from the chain
  - proof_of_work() : work done to mine a new block
  - is_chain_valid : Checks the vlaidity of blockchain.
  
 We use flask to create a simple web application to invoke rest calls
    -/mine_block : For mining a new block in the chain
    -/get_chain : Get the current status of chain, will all the blocks created.
    -/is_valid : To check if the chain is in a vlaid state.
    
  
