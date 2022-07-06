package spittr.backdoor;

import spittr.service.SpittleService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * BackDoorController.
 */
@Controller
@RequestMapping("/_backdoor")
public class BackDoorController {

    private SpittleService spittleService;

    @Autowired
    public BackDoorController(SpittleService spittleService) {
        this.spittleService = spittleService;
    }

    @RequestMapping(value = "/create-spittles", method = RequestMethod.GET)
    @ResponseBody
    public String create() {
        spittleService.create();
        return "create success";
    }
}
