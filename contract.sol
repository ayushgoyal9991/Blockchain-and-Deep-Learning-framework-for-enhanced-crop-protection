pragma solidity >=0.6.0 <0.9.0;

contract Crop_Assister{

	struct Solution{
		address farmer;
        uint256 disease_id;
		string before_pic;
		string after_pic;
		string text;
	}
	Solution[] public Solutions;

	function getSolutionLength() public view returns(uint256){
		return Solutions.length;
	}

	function addSolution(uint256 _id,string memory _before,string memory _after,string memory _text) public{
	    //msg.sender.transfer(10**17); //0.1 ether will be provided as incentive
		Solutions.push(Solution(msg.sender,_id,_before,_after,_text));
	}

	function returnSolutions(uint256 required_id) public view returns(string memory,string memory,string memory,string memory){
        string memory _addresses;
        string memory _before;
        string memory _after;
        string memory _text;
        for (uint256 i=0; i < Solutions.length; i++) {
            if(Solutions[i].disease_id==required_id){
                _addresses=string(abi.encodePacked(_addresses,"  ",toAsciiString(Solutions[i].farmer)));
                _before=string(abi.encodePacked(_before,"  ",Solutions[i].before_pic));
                _after=string(abi.encodePacked(_after,"  ",Solutions[i].after_pic));
                _text=string(abi.encodePacked(_text,"  ",Solutions[i].text));
            }
        }
        return (_addresses,_before,_after,_text);
    }
    
    function toAsciiString(address x) internal pure returns (string memory) {
        bytes memory s = new bytes(40);
        for (uint i = 0; i < 20; i++) {
            bytes1 b = bytes1(uint8(uint(uint160(x)) / (2**(8*(19 - i)))));
            bytes1 hi = bytes1(uint8(b) / 16);
            bytes1 lo = bytes1(uint8(b) - 16 * uint8(hi));
            s[2*i] = char(hi);
            s[2*i+1] = char(lo);            
        }
        return string(s);
    }

    function char(bytes1 b) internal pure returns (bytes1 c) {
        if (uint8(b) < 10) return bytes1(uint8(b) + 0x30);
        else return bytes1(uint8(b) + 0x57);
    }

    function getContractBalance() view public returns(uint256){
    	return address(this).balance;
    }

    function fund() payable public{
    }

    function giveIncentive(address payable one) public payable returns(address){
    	one.send(4*10**17); //0.4 ether 
    }

    function pay_ml() payable public{
		require(msg.value==10**17); //0.1 ether for ml node to predict
	}

	function pay_for_solution() payable public{
		require(msg.value==10**18); //1 ether to pay directly for solution
	}
}